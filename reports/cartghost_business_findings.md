# CartGhost — Business Findings Report

## 1. Executive Summary

CartGhost analyzes a synthetic e-commerce dataset containing 13,000 orders dated between January 1 and October 22, 2026.

The analysis examines order outcomes, completed order value, monthly changes, category performance, and a rule-based potential churn segment.

Completed orders accounted for 87.95% of all orders. March recorded the highest completed order volume and total completed order value among complete months. Snacks ranked highest by completed order value. The potential churn rule identified 1,097 customers among 2,470 customers with at least one completed order.

These results demonstrate an analytical workflow; they are not evidence of actual business performance.

## 2. Dataset Overview

- Total orders: 13,000
- Unique customers with at least one completed order: 2,470
- Analysis date for potential churn: October 22, 2026
- Potential churn inactivity threshold: 45 days
- Minimum completed orders for potential churn qualification: 2

The dataset is synthetic.

## 3. Order Status Analysis

| Status | Order count | Percentage |
|---|---:|---:|
| Completed | 11,433 | 87.95% |
| Cancelled | 1,038 | 7.98% |
| Returned | 529 | 4.07% |
| **Total** | **13,000** | **100.00%** |

### Finding

Completed orders made up 87.95% of all orders. Cancelled and returned orders combined represented 12.05%.

### Business interpretation

In a real e-commerce setting, cancellation and return rates could be investigated further to identify potential opportunities to improve customer experience or order fulfilment. The synthetic dataset does not establish the causes of these outcomes.

## 4. Completed Order Performance

| Metric | Result |
|---|---:|
| Completed orders | 11,433 |
| Unique customers with completed orders | 2,470 |
| Total completed order value | 14,908,918.65 |
| Average completed order value | 1,304.03 |

### Finding

The average completed order value was 1,304.03 units of the dataset's unspecified currency.

### Business interpretation

In a real business, average order value could be tracked over time and compared across categories or customer segments. Further analysis would be required before recommending changes to pricing, product bundles, or promotions.

## 5. Monthly Trends

| Month | Completed orders | Unique customers | Total order value | Average order value |
|---|---:|---:|---:|---:|
| Jan | 1,196 | 962 | 1,533,371.48 | 1,282.08 |
| Feb | 1,095 | 890 | 1,439,695.44 | 1,314.79 |
| Mar | 1,225 | 971 | 1,593,022.70 | 1,300.43 |
| Apr | 1,206 | 986 | 1,582,957.54 | 1,312.57 |
| May | 1,177 | 949 | 1,545,735.92 | 1,313.28 |
| Jun | 1,169 | 935 | 1,550,207.07 | 1,326.10 |
| Jul | 1,198 | 944 | 1,541,463.02 | 1,286.70 |
| Aug | 1,189 | 953 | 1,540,703.93 | 1,295.80 |
| Sep | 1,095 | 887 | 1,437,122.97 | 1,312.44 |
| Oct* | 883 | 757 | 1,144,638.58 | 1,296.31 |

*October data ends on October 22, 2026.*

### Findings

- March had the highest completed order volume, at 1,225.
- March also had the highest total completed order value, at 1,593,022.70.
- June had the highest average order value, at 1,326.10.
- September had 1,095 completed orders, matching February.
- October's totals are incomplete and should not be directly compared with full months.

## 6. Month-over-Month Analysis

| Month | Order change (%) | Order value change (%) |
|---|---:|---:|
| Jan | — | — |
| Feb | -8.44% | -6.11% |
| Mar | +11.87% | +10.65% |
| Apr | -1.55% | -0.63% |
| May | -2.40% | -2.35% |
| Jun | -0.68% | +0.29% |
| Jul | +2.48% | -0.56% |
| Aug | -0.75% | -0.05% |
| Sep | -7.91% | -6.72% |
| Oct* | -19.36% | -20.35% |

*October is a partial month, so its decline relative to September is not a like-for-like comparison.*

### Findings

- February experienced a decline in both completed orders and total order value compared with January.
- March showed the strongest month-over-month rebound, with order volume rising 11.87% and total order value rising 10.65%.
- April through August showed smaller fluctuations in order volume and value.
- September recorded another decline in both measures.
- October's apparent decline must be interpreted cautiously because the month is incomplete.

### Business interpretation

A real business could compare monthly movements with marketing campaigns, seasonality, stock availability, and customer activity. Those explanations cannot be established from this synthetic dataset alone.

## 7. Product Category Performance

| Category | Completed orders | Unique customers | Total order value | Average order value |
|---|---:|---:|---:|---:|
| Snacks | 1,970 | 1,340 | 2,589,313.03 | 1,314.37 |
| Personal Care | 1,954 | 1,362 | 2,528,592.18 | 1,294.06 |
| Dairy | 1,911 | 1,331 | 2,486,311.75 | 1,301.05 |
| Grocery | 1,857 | 1,314 | 2,449,825.66 | 1,319.24 |
| Household | 1,868 | 1,311 | 2,437,259.39 | 1,304.74 |
| Beverages | 1,873 | 1,330 | 2,417,616.64 | 1,290.77 |

### Findings

- Snacks ranked first by completed order count and total completed order value.
- Personal Care ranked second by total completed order value.
- Grocery had the second-highest average order value, at 1,319.24, after Snacks at 1,314.37? 

*Check the category results before final publication: Grocery's reported average order value of 1,319.24 is higher than Snacks' 1,314.37, so Grocery ranks first by average order value.*

### Business interpretation

In a real business, category-level results could inform further investigation into product availability, customer preferences, and merchandising. The generated data does not establish real consumer preferences.

## 8. Potential Customer Churn Analysis

### Definition

A customer is classified as potentially churned when both conditions are met:

1. They have at least two completed orders.
2. Their most recent completed order was at least 45 days before October 22, 2026.

### Results

| Customer status | Customer count | Percentage |
|---|---:|---:|
| Potentially Churned | 1,097 | 44.41% |
| Active / Not Yet Qualified | 1,373 | 55.59% |
| **Total** | **2,470** | **100.00%** |

### Finding

The rule classified 1,097 of the 2,470 customers with at least one completed order as potentially churned.

### Business interpretation

In a real business, this segment could be investigated to understand inactivity and evaluate possible re-engagement strategies. The classification is not a machine-learning prediction and does not prove that customers have permanently churned.

Customers with no completed orders are not included in this summary.

## 9. Recommendations and Further Investigation

Based on the analytical workflow, the following are possible next steps for a real-world dataset:

1. Investigate the reasons for cancelled and returned orders.
2. Monitor monthly order volume and order value using complete-month comparisons.
3. Explore why category performance differs.
4. Test whether the 45-day inactivity threshold is useful for identifying customers who later stop purchasing.
5. Evaluate re-engagement strategies against a suitable comparison group before claiming business impact.

These are proposed investigations, not conclusions proven by the synthetic data.

## 10. Limitations

- All records are synthetic and do not reflect actual customer behavior.
- October covers only the period through October 22, 2026.
- The churn segment is rule-based.
- The dataset's currency unit is unspecified.
- The analysis identifies patterns in generated records but cannot establish causation.

## 11. Tools Used

- Python
- pandas and NumPy
- Matplotlib
- PostgreSQL
- SQL aggregation and window functions
- Git and GitHub

## 12. Conclusion

CartGhost demonstrates an end-to-end analytics workflow that includes data validation, order performance analysis, monthly trend analysis, category comparison, and rule-based customer segmentation.

The project highlights the importance of accurate metric definitions, careful interpretation of incomplete periods, and transparent communication of data limitations.
