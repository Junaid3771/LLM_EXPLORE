# 🧠 LLM Explore Apps

This repository now contains multiple Streamlit demos:

- **Word Embedding Visualizer** (`word_embedding.py`)
- **BERT Attention Arrows Demo** (`attention.py`)
- **Data Analyst Chat Bot** (`data_analyst_chatbot.py`)

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run an App

```bash
streamlit run word_embedding.py
```

```bash
streamlit run attention.py
```

```bash
streamlit run data_analyst_chatbot.py
```

---

## 📊 Data Analyst Chat Bot

The data analyst bot includes SQL table creation code in `create_sales_table.sql` and auto-loads it into a local SQLite database (`sales_demo.db`) on first run.

### Example prompts
- `total sales`
- `sales by region`
- `monthly revenue trend`
- `average order value`
- `top 3 products by revenue`

---

## 📁 Files

- `word_embedding.py`: Embedding visualizer app.
- `attention.py`: Attention graph app.
- `data_analyst_chatbot.py`: SQL-backed chatbot app.
- `create_sales_table.sql`: Table creation + seed data script.
