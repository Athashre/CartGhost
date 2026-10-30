
/*
========================================================
PROJECT: CARTGHOST
TITLE: E-commerce Data Analysis
DATABASE: PostgreSQL
DATASET: Synthetic E-commerce Orders
ANALYSIS DATE: October 22, 2026

OBJECTIVES:
1. Explore the dataset.
2. Validate data quality.
3. Analyze order status and performance.
4. Analyze monthly trends and growth.
5. Compare category performance.
6. Analyze customer purchase history.
7. Identify potentially churned customers.
8. Identify highest-value orders.
========================================================
*/


/* ======================================================
   1. DATASET OVERVIEW
   ====================================================== */

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders;


/* ======================================================
   2. DATA QUALITY CHECKS
   ====================================================== */

SELECT
    COUNT(*) FILTER (
        WHERE order_id IS NULL
    ) AS missing_order_ids,

    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS missing_customer_ids,

    COUNT(*) FILTER (
        WHERE order_date IS NULL
    ) AS missing_order_dates,

    COUNT(*) FILTER (
        WHERE status IS NULL
    ) AS missing_statuses,

    COUNT(*) FILTER (
        WHERE order_value IS NULL
    ) AS missing_order_values,

    COUNT(*) FILTER (
        WHERE order_value < 0
    ) AS negative_order_values,

    COUNT(*) - COUNT(DISTINCT order_id)
        AS duplicate_order_ids

FROM orders;


/* Check duplicate order IDs explicitly */

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


/* ======================================================
   3. ORDER STATUS BREAKDOWN
   ====================================================== */

SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM orders
GROUP BY status
ORDER BY order_count DESC;


/* ======================================================
   4. COMPLETED ORDER PERFORMANCE
   ====================================================== */

SELECT
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(order_value), 2) AS total_order_value,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
WHERE status = 'Completed';


/* ======================================================
   5. MONTHLY ORDER TRENDS
   ====================================================== */

SELECT
    DATE_TRUNC('month', order_date)::DATE AS month,
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(order_value), 2) AS total_order_value,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
WHERE status = 'Completed'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


/* ======================================================
   6. MONTH-OVER-MONTH GROWTH
   ====================================================== */

WITH monthly AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS month,
        COUNT(*) AS completed_orders,
        SUM(order_value) AS total_order_value
    FROM orders
    WHERE status = 'Completed'
    GROUP BY DATE_TRUNC('month', order_date)
),

comparison AS (
    SELECT
        month,
        completed_orders,
        total_order_value,

        LAG(completed_orders) OVER (
            ORDER BY month
        ) AS previous_orders,

        LAG(total_order_value) OVER (
            ORDER BY month
        ) AS previous_order_value

    FROM monthly
)

SELECT
    month,
    completed_orders,

    ROUND(total_order_value, 2)
        AS total_order_value,

    completed_orders - previous_orders
        AS order_change,

    ROUND(
        100.0 * (completed_orders - previous_orders)
        / NULLIF(previous_orders, 0),
        2
    ) AS order_growth_pct,

    ROUND(
        total_order_value - previous_order_value,
        2
    ) AS value_change,

    ROUND(
        100.0 * (total_order_value - previous_order_value)
        / NULLIF(previous_order_value, 0),
        2
    ) AS value_growth_pct

FROM comparison
ORDER BY month;


/* ======================================================
   7. CATEGORY-WISE ORDER PERFORMANCE
   ====================================================== */

SELECT
    category,
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(order_value), 2) AS total_order_value,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
WHERE status = 'Completed'
GROUP BY category
ORDER BY total_order_value DESC;


/* ======================================================
   8. CUSTOMER-LEVEL PURCHASE HISTORY
   ====================================================== */

SELECT
    customer_id,
    COUNT(*) AS completed_orders,
    ROUND(SUM(order_value), 2) AS total_order_value,
    ROUND(AVG(order_value), 2) AS average_order_value,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders
WHERE status = 'Completed'
GROUP BY customer_id
ORDER BY total_order_value DESC;


/* ======================================================
   9. IDENTIFY POTENTIALLY CHURNED CUSTOMERS
   ====================================================== */

WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_orders,
        MAX(order_date) AS last_order_date
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
)

SELECT
    customer_id,
    completed_orders,
    last_order_date,

    DATE '2026-10-22' - last_order_date
        AS days_inactive

FROM customer_activity

WHERE completed_orders >= 2
  AND DATE '2026-10-22' - last_order_date >= 45

ORDER BY days_inactive DESC;


/* ======================================================
   10. POTENTIAL CUSTOMER CHURN SUMMARY
   ====================================================== */

WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_orders,
        MAX(order_date) AS last_order_date
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
),

customer_status AS (
    SELECT
        customer_id,

        CASE
            WHEN completed_orders >= 2
             AND DATE '2026-10-22' - last_order_date >= 45
            THEN 'Potentially Churned'

            ELSE 'Active / Not Yet Qualified'
        END AS customer_status

    FROM customer_activity
)

SELECT
    customer_status,
    COUNT(*) AS customer_count,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM customer_status
GROUP BY customer_status
ORDER BY customer_count DESC;


/* ======================================================
   11. HIGHEST-VALUE COMPLETED ORDERS
   ====================================================== */

SELECT
    order_id,
    customer_id,
    order_date,
    category,
    order_value
FROM orders
WHERE status = 'Completed'
ORDER BY order_value DESC
LIMIT 10;


/* ======================================================
   12. FINAL ORDER STATUS VERIFICATION
   ====================================================== */

SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(order_value), 2) AS total_order_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;


/* ======================================================
   END OF CARTGHOST SQL ANALYSIS
   ====================================================== */
