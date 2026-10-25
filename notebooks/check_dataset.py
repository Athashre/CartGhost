
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

INPUT_FILE = DATA_DIR / "synthetic_orders_2026.csv"

# Load the dataset
orders = pd.read_csv(INPUT_FILE, parse_dates=["order_date"])

print("\nCARTGHOST — DATA QUALITY REPORT")
print("=" * 50)

# 1. Dataset dimensions
print("\n1. Dataset size")
print("Rows:", orders.shape[0])
print("Columns:", orders.shape[1])

# 2. Required columns
required_columns = [
    "order_id",
    "customer_id",
    "order_date",
    "status",
    "order_value",
    "category",
]

missing_columns = [
    col for col in required_columns if col not in orders.columns
]

if missing_columns:
    print("\nERROR — Missing columns:", missing_columns)
    raise ValueError("Dataset does not contain all required columns.")

print("\n2. Required columns: PASS")

# 3. Missing values
print("\n3. Missing values by column")
print(orders.isna().sum().to_string())

# 4. Duplicate records
print("\n4. Duplicate checks")
print("Duplicate full rows:", orders.duplicated().sum())
print("Duplicate order IDs:", orders["order_id"].duplicated().sum())

# 5. Date range
print("\n5. Order date range")
print("Earliest:", orders["order_date"].min())
print("Latest:", orders["order_date"].max())

# 6. Order statuses
print("\n6. Order status counts")
print(orders["status"].value_counts(dropna=False).to_string())

# 7. Order values
print("\n7. Order value checks")
print("Missing order values:", orders["order_value"].isna().sum())
print("Negative order values:", (orders["order_value"] < 0).sum())
print("Minimum order value:", orders["order_value"].min())
print("Maximum order value:", orders["order_value"].max())

# 8. Unique customers and orders
print("\n8. Unique counts")
print("Unique customers:", orders["customer_id"].nunique())
print("Unique order IDs:", orders["order_id"].nunique())

# 9. Overall quality verdict
checks = {
    "No missing order IDs": orders["order_id"].notna().all(),
    "No duplicate order IDs": orders["order_id"].is_unique,
    "No missing customer IDs": orders["customer_id"].notna().all(),
    "No missing order dates": orders["order_date"].notna().all(),
    "No missing order statuses": orders["status"].notna().all(),
    "No missing order values": orders["order_value"].notna().all(),
    "No negative order values": (orders["order_value"].dropna() >= 0).all(),
}

print("\n9. Validation results")
for check_name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} — {check_name}")

print("\nNote: This dataset is synthetic.")
