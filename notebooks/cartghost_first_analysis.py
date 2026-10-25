
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Fixed date makes our analysis reproducible
ANALYSIS_DATE = pd.Timestamp("2026-10-22")
INACTIVITY_DAYS = 45

# Small SYNTHETIC practice dataset (not real business data)
orders = pd.DataFrame([
    ("O001", "C001", "2025-10-01", "Completed", "Grocery"),
    ("O002", "C001", "2025-11-01", "Completed", "Dairy"),
    ("O003", "C002", "2025-11-01", "Completed", "Snacks"),
    ("O004", "C002", "2025-12-01", "Completed", "Grocery"),
    ("O005", "C003", "2025-09-01", "Completed", "Personal Care"),
    ("O006", "C004", "2025-09-01", "Completed", "Grocery"),
    ("O007", "C004", "2025-10-01", "Completed", "Snacks"),
    ("O008", "C005", "2025-08-01", "Completed", "Dairy"),
    ("O009", "C005", "2025-12-15", "Cancelled", "Grocery"),
], columns=["order_id", "customer_id", "order_date",
            "status", "category"])

orders["order_date"] = pd.to_datetime(orders["order_date"])

# Save practice data for later use
orders.to_csv(DATA_DIR / "practice_orders.csv", index=False)

# Only completed orders count toward customer activity
completed = orders[orders["status"] == "Completed"].copy()

# Summarize each customer's completed orders
customers = completed.groupby("customer_id").agg(
    completed_orders=("order_id", "count"),
    last_order_date=("order_date", "max")
).reset_index()

# Calculate days since last completed order
customers["days_since_last_order"] = (
    ANALYSIS_DATE - customers["last_order_date"]
).dt.days

# Apply CartGhost's business rule
customers["potentially_churned"] = (
    (customers["completed_orders"] >= 2)
    & (
        customers["days_since_last_order"]
        >= INACTIVITY_DAYS
    )
)
customers["customer_status"] = customers[
    "potentially_churned"
].map({
    True: "Potentially Churned",
    False: "Active / Not Yet Qualified"
})

# Display results
print("\nCARTGHOST — CUSTOMER CHURN ANALYSIS")
print("Analysis date:", ANALYSIS_DATE.date())
print("-" * 65)
print(customers.to_string(index=False))

# Save results for our future dashboard
customers.to_csv(DATA_DIR / "customer_churn_results.csv", index=False)

print("\nPractice data saved to the data folder.")
print("Customer results saved to the data folder.")



# STEP 10: DATA QUALITY CHECKS

print("\n--- DATA QUALITY CHECKS ---")

# Check for missing values
print("\nMissing values in order data:")
print(orders.isnull().sum())

# Check for duplicate order IDs
print("\nDuplicate order IDs:")
print(orders["order_id"].duplicated().sum())

# Check order status counts
print("\nOrder status counts:")
print(orders["status"].value_counts())

# Check whether completed order dates are valid
print("\nOrders dated after analysis date:")
print((completed["order_date"] > ANALYSIS_DATE).sum())

# Validate customer churn rules
assert (customers["completed_orders"] >= 1).all()
assert (customers["days_since_last_order"] >= 0).all()

expected_churn = (
    (customers["completed_orders"] >= 2)
    & (customers["days_since_last_order"] >= INACTIVITY_DAYS)
)

assert (
    customers["potentially_churned"] == expected_churn
).all()

print("\nAll basic validation checks passed!")
