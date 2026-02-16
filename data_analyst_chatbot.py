import re
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path("sales_demo.db")
SQL_BOOTSTRAP_PATH = Path("create_sales_table.sql")


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    initialize_database(conn)
    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    has_sales_table = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='sales'"
    ).fetchone()

    if has_sales_table:
        return

    bootstrap_sql = SQL_BOOTSTRAP_PATH.read_text(encoding="utf-8")
    conn.executescript(bootstrap_sql)
    conn.commit()


def extract_top_n(text: str, default_n: int = 5) -> int:
    match = re.search(r"top\s+(\d+)", text)
    return int(match.group(1)) if match else default_n


def build_query(user_prompt: str) -> tuple[str, str]:
    prompt = user_prompt.lower().strip()

    if "top" in prompt and ("product" in prompt or "products" in prompt):
        top_n = extract_top_n(prompt)
        return (
            f"""
            SELECT product_name,
                   ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
            FROM sales
            GROUP BY product_name
            ORDER BY revenue DESC
            LIMIT {top_n}
            """,
            f"Ranked top {top_n} products by total revenue.",
        )

    if any(phrase in prompt for phrase in ["total sales", "overall sales", "revenue"]):
        return (
            """
            SELECT ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS total_revenue
            FROM sales
            """,
            "Calculated total net revenue after discounts.",
        )

    if "sales by region" in prompt or ("region" in prompt and "sales" in prompt):
        return (
            """
            SELECT region,
                   ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
            FROM sales
            GROUP BY region
            ORDER BY revenue DESC
            """,
            "Grouped revenue by region and sorted from highest to lowest.",
        )

    if "monthly" in prompt or "month" in prompt or "trend" in prompt:
        return (
            """
            SELECT substr(order_date, 1, 7) AS month,
                   ROUND(SUM(quantity * unit_price * (1 - discount)), 2) AS revenue
            FROM sales
            GROUP BY month
            ORDER BY month
            """,
            "Summarized revenue by month to show trend over time.",
        )

    if "average order value" in prompt or "aov" in prompt:
        return (
            """
            SELECT ROUND(AVG(order_value), 2) AS average_order_value
            FROM (
                SELECT order_id,
                       SUM(quantity * unit_price * (1 - discount)) AS order_value
                FROM sales
                GROUP BY order_id
            )
            """,
            "Computed average value per order after discount.",
        )

    return (
        """
        SELECT order_id, order_date, customer_name, region, product_name,
               quantity, unit_price, discount,
               ROUND(quantity * unit_price * (1 - discount), 2) AS net_line_revenue
        FROM sales
        ORDER BY order_date
        LIMIT 20
        """,
        "I could not map the question to a predefined analysis intent, so I returned sample transaction rows.",
    )


def display_chart(df: pd.DataFrame) -> None:
    if {"region", "revenue"}.issubset(df.columns):
        fig = px.bar(df, x="region", y="revenue", title="Revenue by Region")
        st.plotly_chart(fig, use_container_width=True)

    if {"month", "revenue"}.issubset(df.columns):
        fig = px.line(df, x="month", y="revenue", markers=True, title="Monthly Revenue Trend")
        st.plotly_chart(fig, use_container_width=True)

    if {"product_name", "revenue"}.issubset(df.columns):
        fig = px.bar(df, x="product_name", y="revenue", title="Top Product Revenue")
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Data Analyst Chat Bot", layout="wide")
    st.title("📊 Data Analyst Chat Bot")
    st.caption("Ask business questions and get SQL-backed answers from a demo sales table.")

    with st.expander("How this bot works"):
        st.markdown(
            """
            - Uses **SQLite** as the analytics database.
            - Automatically runs `create_sales_table.sql` once to build the table and insert sample rows.
            - Converts common analysis prompts into SQL queries.
            """
        )

    with st.sidebar:
        st.subheader("Example prompts")
        st.markdown(
            """
            - total sales
            - sales by region
            - monthly revenue trend
            - average order value
            - top 3 products by revenue
            """
        )

    conn = get_connection()

    question = st.text_input("Ask your analysis question")

    if st.button("Run Analysis"):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        sql, explanation = build_query(question)
        st.markdown("### Generated SQL")
        st.code(sql.strip(), language="sql")

        df = pd.read_sql_query(sql, conn)

        st.markdown("### Insight")
        st.write(explanation)

        st.markdown("### Result")
        st.dataframe(df, use_container_width=True)

        display_chart(df)


if __name__ == "__main__":
    main()
