
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

# Load the synthetic orders dataset
orders = pd.read_csv(
    DATA_DIR / "synthetic_orders_2026.csv",
    parse_dates=["order_date"]
)

# Basic validation
required_columns = [
    "order_id", "customer_id", "order_date",
    "status", "order_value"
]

missing_columns = [
    col for col in required_columns if col not in orders.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Analyze completed orders only
completed = orders.loc[
    orders["status"] == "Completed"
].copy()

if completed.empty:
    raise ValueError("No completed orders found in the dataset.")

# Create calendar-month groups
completed["month"] = (
    completed["order_date"].dt.to_period("M").astype(str)
)

monthly = completed.groupby("month").agg(
    completed_orders=("order_id", "count"),
    unique_customers=("customer_id", "nunique"),
    total_order_value=("order_value", "sum"),
    average_order_value=("order_value", "mean")
).reset_index()

# Ensure months are in chronological order
monthly = monthly.sort_values("month").reset_index(drop=True)

# Calculate month-over-month changes
monthly["order_change"] = monthly["completed_orders"].diff()
monthly["order_mom_pct"] = (
    monthly["completed_orders"].pct_change() * 100
).round(2)

monthly["order_value_change"] = (
    monthly["total_order_value"].diff().round(2)
)

monthly["order_value_mom_pct"] = (
    monthly["total_order_value"].pct_change() * 100
).round(2)

# Round metrics for readability
monthly["total_order_value"] = (
    monthly["total_order_value"].round(2)
)

monthly["average_order_value"] = (
    monthly["average_order_value"].round(2)
)

# Save the combined monthly analysis
output_file = DATA_DIR / "monthly_trends_2026.csv"
monthly.to_csv(output_file, index=False)

# Print the monthly summary
print("\nCARTGHOST — MONTHLY ORDER TRENDS")
print("=" * 75)
print(monthly.to_string(index=False))

print("\nOVERALL SUMMARY")
print("-" * 40)
print("Total completed orders:", len(completed))
print("Unique customers:", completed["customer_id"].nunique())
print(
    "Total completed order value:",
    round(completed["order_value"].sum(), 2)
)
print(
    "Average order value:",
    round(completed["order_value"].mean(), 2)
)

# Plot completed orders and order value by month
fig, axes = plt.subplots(2, 1, figsize=(11, 8))

axes[0].plot(
    monthly["month"],
    monthly["completed_orders"],
    marker="o"
)
axes[0].set_title("Monthly Completed Orders")
axes[0].set_ylabel("Number of orders")
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis="x", rotation=45)

axes[1].plot(
    monthly["month"],
    monthly["total_order_value"],
    marker="o"
)
axes[1].set_title("Monthly Completed Order Value")
axes[1].set_ylabel("Order value")
axes[1].set_xlabel("Month")
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis="x", rotation=45)

plt.tight_layout()

# Save the chart in the existing reports folder
chart_file = PROJECT_DIR / "reports" / "monthly_trends_2026.png"
plt.savefig(chart_file, dpi=150, bbox_inches="tight")
plt.show()

print("\nSaved monthly data:", output_file)
print("Saved chart:", chart_file)
print("Note: All order data is synthetic, not real business data.")
