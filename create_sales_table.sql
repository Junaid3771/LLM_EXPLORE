DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    order_id INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    discount REAL NOT NULL DEFAULT 0 CHECK(discount >= 0 AND discount <= 1)
);

INSERT INTO sales (order_id, order_date, customer_name, region, product_category, product_name, quantity, unit_price, discount)
VALUES
    (1001, '2024-01-05', 'Acme Corp', 'North', 'Software', 'Analytics Pro', 2, 1200.00, 0.05),
    (1002, '2024-01-08', 'Beta LLC', 'West', 'Hardware', 'Data Gateway', 5, 350.00, 0.00),
    (1003, '2024-02-10', 'City Retail', 'South', 'Software', 'Insight Hub', 1, 2000.00, 0.10),
    (1004, '2024-02-14', 'Delta Services', 'East', 'Training', 'BI Workshop', 10, 150.00, 0.00),
    (1005, '2024-03-02', 'Evergreen Inc', 'North', 'Hardware', 'Sensor Pack', 8, 95.00, 0.15),
    (1006, '2024-03-15', 'Futura Labs', 'West', 'Software', 'Forecast AI', 3, 950.00, 0.00),
    (1007, '2024-04-01', 'Gamma Group', 'South', 'Services', 'Implementation', 1, 5000.00, 0.00),
    (1008, '2024-04-18', 'Helios Co', 'East', 'Software', 'Analytics Pro', 4, 1200.00, 0.08),
    (1009, '2024-05-04', 'Ion Dynamics', 'North', 'Services', 'Support Plan', 6, 400.00, 0.00),
    (1010, '2024-05-20', 'Juno Systems', 'West', 'Training', 'Data Literacy', 12, 90.00, 0.00),
    (1011, '2024-06-06', 'Kappa Foods', 'South', 'Hardware', 'Data Gateway', 7, 350.00, 0.05),
    (1012, '2024-06-22', 'Lumen Health', 'East', 'Software', 'Insight Hub', 2, 2000.00, 0.07);
