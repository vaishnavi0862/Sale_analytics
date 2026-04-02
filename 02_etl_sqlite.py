"""
Load Excel staging files into SQLite (analytics warehouse).
Creates dim_date from the order date range. Run after 01_generate_excel_data.py
"""
from __future__ import annotations

import sqlite3
from calendar import month_name
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "database"
DB_PATH = DB_DIR / "sales.db"
SCHEMA_PATH = ROOT / "sql" / "01_schema.sql"


def build_date_dimension(conn: sqlite3.Connection, dmin: date, dmax: date) -> None:
    rows = []
    d = dmin
    while d <= dmax:
        rows.append(
            (
                d.isoformat(),
                d.isoformat(),
                d.year,
                (d.month - 1) // 3 + 1,
                d.month,
                month_name[d.month],
                d.weekday(),
                1 if d.weekday() >= 5 else 0,
            )
        )
        d += timedelta(days=1)
    conn.executemany(
        """INSERT OR REPLACE INTO dim_date
        (date_key, full_date, year, quarter, month, month_name, day_of_week, is_weekend)
        VALUES (?,?,?,?,?,?,?,?)""",
        rows,
    )


def main() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    customers = pd.read_excel(DATA_DIR / "customers.xlsx")
    products = pd.read_excel(DATA_DIR / "products.xlsx")
    sales = pd.read_excel(DATA_DIR / "sales_line_items.xlsx")

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    customers.to_sql("dim_customer", conn, if_exists="append", index=False)
    products.to_sql("dim_product", conn, if_exists="append", index=False)
    sales.to_sql("fact_sales", conn, if_exists="append", index=False)

    dates = pd.to_datetime(sales["order_date"])
    dmin = dates.min().date()
    dmax = dates.max().date()
    build_date_dimension(conn, dmin, dmax)

    conn.commit()
    conn.close()
    print(f"SQLite database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
