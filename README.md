# CartGhost — E-commerce Data Analytics

## Project Overview

CartGhost is a data analytics portfolio project exploring e-commerce order performance, monthly trends, product categories, and potential customer churn using Python and PostgreSQL.

**Note:** The dataset is synthetic and is used for educational and portfolio purposes.

## Business Objectives

- Analyze completed, cancelled, and returned orders.
- Measure completed order value and average order value.
- Track monthly order volume and order-value changes.
- Compare completed-order performance across categories.
- Identify customers meeting a rule-based potential churn definition.

## Tools and Technologies

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- PostgreSQL
- SQL
- Git

## Project Structure

```text
CartGhost/
├── data/
│   ├── synthetic_orders_2026.csv
│   ├── monthly_trends_2026.csv
│   └── customer_churn_results_2026.csv
├── notebooks/
│   ├── cartghost_setup.py
│   ├── cartghost_first_analysis.py
│   ├── check_dataset.py
│   ├── generate_synthetic_data.py
│   ├── analyze_churn_2026.py
│   └── monthly_trends.py
├── sql/
│   └── cartghost_analysis.sql
├── reports/
│   └── monthly_trends_2026.png
└── README.md
```

*This structure describes the intended deliverables; adjust it to match the files actually present in your project.*

## Analysis Methodology

1. Validate the dataset and check for common data-quality issues.
2. Analyze order status and completed-order performance.
3. Aggregate completed orders by month.
4. Compare monthly performance using month-over-month calculations.
5. Segment customers using a defined inactivity rule.

## Potential Churn Definition

A customer is classified as potentially churned if they have at least two completed orders and their last completed order was at least 45 days before October 22, 2026.

This is a rule-based classification, not a machine-learning prediction.

## Key Findings

*Add verified findings from your SQL and Python outputs here.*

## Limitations

The dataset is synthetic. Results do not establish real-world customer behavior, revenue trends, or business outcomes.

## Future Improvements

- Add a dashboard.
- Compare customer retention across categories.
- Test alternative inactivity thresholds.
- Add automated data-quality checks.
