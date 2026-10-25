
from pathlib import Path
import numpy as np
import pandas as pd

# Reproducible synthetic dataset
rng = np.random.default_rng(42)

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Dataset settings
NUM_ORDERS = 13_000
NUM_CUSTOMERS = 2_500

START_DATE = "2026-01-01"
END_DATE = "2026-10-22"

# Generate order dates, customer IDs, and categories
dates = pd.date_range(START_DATE, END_DATE, freq="D")

orders = pd.DataFrame({
    "order_id": [
        f"ORD{i:06d}" for i in range(1, NUM_ORDERS + 1)
    ],
    "customer_id": [
        f"CUST{i:05d}"
        for i in rng.integers(1, NUM_CUSTOMERS + 1, NUM_ORDERS)
    ],
    "order_date": rng.choice(dates, size=NUM_ORDERS),
    "status": rng.choice(
        ["Completed", "Cancelled", "Returned"],
        size=NUM_ORDERS,
        p=[0.88, 0.08, 0.04]
    ),
    "category": rng.choice(
        ["Grocery", "Dairy", "Snacks", "Beverages",
         "Personal Care", "Household"],
        size=NUM_ORDERS
    ),
    "order_value": np.round(
        rng.uniform(100, 2500, size=NUM_ORDERS), 2
    )
})

# Sort chronologically
orders = orders.sort_values(
    ["order_date", "order_id"]
).reset_index(drop=True)

# Save the synthetic dataset
output_file = DATA_DIR / "synthetic_orders_2026.csv"
orders.to_csv(output_file, index=False)

# Basic summary
print("CARTGHOST — SYNTHETIC DATA GENERATOR")
print("-" * 40)
print("Total orders:", len(orders))
print("Unique customers:", orders["customer_id"].nunique())
print("Start date:", orders["order_date"].min().date())
print("End date:", orders["order_date"].max().date())
print("\nOrder status breakdown:")
print(orders["status"].value_counts())
print("\nSaved dataset to:", output_file)
print("\nNote: This is synthetic data, not real transactions.")
