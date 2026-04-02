"""
Mirror key SQL analytics with pandas (ad-hoc Python layer).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "sales.db"


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Missing {DB_PATH}. Run scripts/02_etl_sqlite.py first.")

    conn = sqlite3.connect(DB_PATH)
    try:
        sales = pd.read_sql("SELECT * FROM fact_sales", conn)
        products = pd.read_sql("SELECT * FROM dim_product", conn)
        customers = pd.read_sql("SELECT * FROM dim_customer", conn)
    finally:
        conn.close()

    df = sales.merge(products, on="product_id").merge(customers, on="customer_id")
    df["line_revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])
    df["line_margin"] = df["quantity"] * (
        df["unit_price"] * (1 - df["discount_pct"]) - df["unit_cost"]
    )

    df["order_date"] = pd.to_datetime(df["order_date"])
    monthly = (
        df.groupby(df["order_date"].dt.to_period("M"))["line_revenue"]
        .sum()
        .sort_index()
    )
    print("Net revenue by month (Python):")
    print(monthly.to_string())
    print()

    top = (
        df.groupby(["product_name", "category"], as_index=False)["line_revenue"]
        .sum()
        .sort_values("line_revenue", ascending=False)
        .head(5)
    )
    print("Top 5 products by revenue:")
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
