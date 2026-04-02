"""
Generate sample sales source files in Excel (staging layer).
Run from project root: python scripts/01_generate_excel_data.py
"""
from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RANDOM_SEED = 42


def main() -> None:
    random.seed(RANDOM_SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    regions = ["North", "South", "East", "West", "Central"]
    segments = ["Enterprise", "SMB", "Consumer"]

    customers = []
    for i in range(1, 51):
        customers.append(
            {
                "customer_id": i,
                "customer_name": f"Customer {i:03d}",
                "region": random.choice(regions),
                "segment": random.choice(segments),
                "signup_date": (date(2022, 1, 1) + timedelta(days=random.randint(0, 400))).isoformat(),
            }
        )

    categories = ["Electronics", "Furniture", "Office", "Accessories"]
    products = []
    for i in range(1, 31):
        cost = round(random.uniform(5, 120), 2)
        products.append(
            {
                "product_id": i,
                "sku": f"SKU-{i:04d}",
                "product_name": f"Product {i}",
                "category": random.choice(categories),
                "unit_cost": cost,
            }
        )

    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    order_rows = []
    sale_id = 1
    order_num = 1

    for _ in range(800):
        odate = start + timedelta(days=random.randint(0, (end - start).days))
        cust = random.choice(customers)["customer_id"]
        n_lines = random.randint(1, 4)
        oid = f"ORD-{order_num:06d}"
        order_num += 1
        for _ in range(n_lines):
            prod = random.choice(products)
            qty = random.randint(1, 10)
            unit_price = round(prod["unit_cost"] * random.uniform(1.15, 2.2), 2)
            discount = random.choice([0, 0, 0, 0.05, 0.1, 0.15])
            order_rows.append(
                {
                    "sale_id": sale_id,
                    "order_id": oid,
                    "order_date": odate.isoformat(),
                    "customer_id": cust,
                    "product_id": prod["product_id"],
                    "quantity": qty,
                    "unit_price": unit_price,
                    "discount_pct": discount,
                }
            )
            sale_id += 1

    pd.DataFrame(customers).to_excel(DATA_DIR / "customers.xlsx", index=False)
    pd.DataFrame(products).to_excel(DATA_DIR / "products.xlsx", index=False)
    pd.DataFrame(order_rows).to_excel(DATA_DIR / "sales_line_items.xlsx", index=False)

    print(f"Wrote Excel files to {DATA_DIR}")


if __name__ == "__main__":
    main()
