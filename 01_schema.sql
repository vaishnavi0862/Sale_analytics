-- Sales analytics warehouse (SQLite-compatible)
-- Run after loading data, or use Python ETL which creates tables from Excel.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_date (
    date_key TEXT PRIMARY KEY,
    full_date TEXT NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    segment TEXT NOT NULL,
    signup_date TEXT
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_cost REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount_pct REAL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_id);
