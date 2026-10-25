
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

ANALYSIS_DATE = pd.Timestamp("2026-10-22")
INACTIVITY_DAYS = 45
MIN_COMPLETED_ORDERS = 2

INPUT_FILE = DATA_DIR / "synthetic_orders_2026.csv"
OUTPUT_FILE = DATA_DIR / "customer_churn_results_2026.csv"

# Load synthetic orders
orders = pd.read_csv(INPUT_FILE, parse_dates=["order_date"])

# Validate required columns
required_columns = [
    "order_id", "customer_id", "order_date",
    "status", "order_value"
]

missing_columns = [
    column for column in required_columns
    if column not in orders.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

if orders.empty:
    raise ValueError("The dataset contains no orders.")

if orders["order_id"].isna().any():
    raise ValueError("Missing order IDs found.")

if not orders["order_id"].is_unique:
    raise ValueError("Duplicate order IDs found.")

if orders["customer_id"].isna().any():
    raise ValueError("Missing customer IDs found.")

if orders["order_date"].isna().any():
    raise ValueError("Missing or invalid order dates found.")

if (orders["order_date"] > ANALYSIS_DATE).any():
    raise ValueError("Orders after the analysis date found.")

if (orders["order_value"].dropna() < 0).any():
    raise ValueError("Negative order values found; review the data.")

# Keep completed orders for activity calculations
completed = orders.loc[
    orders["status"] == "Completed"
].copy()

# Start with every customer present in the dataset
customers = (
    orders[["customer_id"]]
    .drop_duplicates()
    .copy()
)

# Calculate completed-order activity for each customer
activity = completed.groupby("customer_id").agg(
    completed_orders=("order_id", "count"),
    last_order_date=("order_date", "max")
).reset_index()

# Join activity back so customers with zero completed orders remain
customers = customers.merge(
    activity,
    on="customer_id",
    how="left"
)

customers["completed_orders"] = (
    customers["completed_orders"].fillna(0).astype(int)
)

# Calculate days since last completed order
customers["days_since_last_order"] = (
    ANALYSIS_DATE - customers["last_order_date"]
).dt.days.astype("Int64")

# Apply the rule: at least 2 completed orders AND 45+ inactive days
customers["potentially_churned"] = (
    (customers["completed_orders"] >= MIN_COMPLETED_ORDERS)
    & (customers["days_since_last_order"] >= INACTIVITY_DAYS)
)

# Assign clear customer segments
conditions = [
    customers["completed_orders"] == 0,
    customers["completed_orders"] < MIN_COMPLETED_ORDERS,
    customers["potentially_churned"],
]

labels = [
    "No Completed Orders",
    "Insufficient Order History",
    "Potentially Churned",
]

customers["customer_status"] = pd.Series(
    pd.NA, index=customers.index, dtype="string"
)

for condition, label in zip(conditions, labels):
    customers.loc[condition, "customer_status"] = label

customers.loc[
    customers["customer_status"].isna(),
    "customer_status"
] = "Active / Not Yet Qualified"

# Put potential churn cases first, then sort by inactivity
customers = customers.sort_values(
    ["potentially_churned", "days_since_last_order"],
    ascending=[False, False],
    na_position="last"
).reset_index(drop=True)

# Save customer-level results
customers.to_csv(OUTPUT_FILE, index=False)

# Report summary
eligible_customers = customers[
    customers["completed_orders"] >= MIN_COMPLETED_ORDERS
]

potential_churn_count = int(
    customers["potentially_churned"].sum()
)

eligible_count = len(eligible_customers)

potential_churn_rate = (
    potential_churn_count / eligible_count * 100
    if eligible_count > 0 else 0
)

print("\nCARTGHOST — 2026 CHURN REPORT")
print("=" * 50)
print("Analysis date:", ANALYSIS_DATE.date())
print("Inactivity threshold:", INACTIVITY_DAYS, "days")
print("Minimum completed orders:", MIN_COMPLETED_ORDERS)
print("Total order records:", len(orders))
print("Completed order records:", len(completed))
print("All customers in dataset:", len(customers))
print("Customers with completed orders:", int(
    (customers["completed_orders"] > 0).sum()
))
print("Customers eligible for churn rule:", eligible_count)
print("Potentially churned customers:", potential_churn_count)
print(f"Potential churn rate among eligible customers: {potential_churn_rate:.2f}%")

print("\nCUSTOMER STATUS BREAKDOWN")
print("-" * 40)
print(customers["customer_status"].value_counts().to_string())

print("\nSAMPLE POTENTIAL CHURN CASES")
print("-" * 40)

churn_sample = customers.loc[
    customers["potentially_churned"],
    [
        "customer_id",
        "completed_orders",
        "last_order_date",
        "days_since_last_order",
        "customer_status",
    ],
].head(10)

if churn_sample.empty:
    print("No customers met the current rule.")
else:
    print(churn_sample.to_string(index=False))

print("\nSaved:", OUTPUT_FILE)
print("Reminder: results are based on synthetic data and a rule-based definition.")
