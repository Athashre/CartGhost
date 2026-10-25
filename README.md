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

### Order Status

- **Total orders:** 13,000
- **Completed:** 11,433 (87.95%)
- **Cancelled:** 1,038 (7.98%)
- **Returned:** 529 (4.07%)

Most orders in this synthetic dataset were completed. Cancelled and returned orders together accounted for 12.05% of all orders.

### Completed Order Performance

- **Completed orders:** 11,433
- **Unique customers across completed orders:** 2,470
- **Total completed order value:** 14,908,918.65
- **Average value per completed order:** 1,304.03

The average completed order value was 1,304.03 units of the dataset's currency, which has not yet been specified.

### Interpretation

These metrics establish a baseline for evaluating order outcomes and completed-order performance. Further analysis of monthly trends, product categories, and customer inactivity can help explore patterns in the synthetic data.

**Data limitation:** This project uses synthetic data. These figures are illustrative and do not represent the performance of a real business.


## Limitations

The dataset is synthetic. Results do not establish real-world customer behavior, revenue trends, or business outcomes.

## Future Improvements

- Add a dashboard.
- Compare customer retention across categories.
- Test alternative inactivity thresholds.
- Add automated data-quality checks.
