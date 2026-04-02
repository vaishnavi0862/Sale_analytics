"""
Export a denormalized sales table as CSV for Power BI (Get Data > Text/CSV).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "sales.db"
EXPORT_DIR = ROOT / "exports"


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        raise SystemExit(f"Missing {DB_PATH}. Run scripts/02_etl_sqlite.py first.")

    q = """
    SELECT
        f.sale_id,
        f.order_id,
        f.order_date,
        d.year AS order_year,
        d.quarter AS order_quarter,
        d.month_name,
        c.customer_name,
        c.region,
        c.segment,
        p.sku,
        p.product_name,
        p.category,
        p.unit_cost,
        f.quantity,
        f.unit_price,
        f.discount_pct,
        ROUND(f.quantity * f.unit_price * (1 - f.discount_pct), 2) AS line_revenue,
        ROUND(f.quantity * (f.unit_price * (1 - f.discount_pct) - p.unit_cost), 2) AS line_margin
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    JOIN dim_product p ON f.product_id = p.product_id
    LEFT JOIN dim_date d ON f.order_date = d.date_key
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(q, conn)
    finally:
        conn.close()
    out = EXPORT_DIR / "sales_fact_denormalized.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
