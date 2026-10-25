/* Check the dataset*/
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders;


/*2. Check data quality*/
SELECT
    COUNT(*) FILTER (WHERE order_id IS NULL) AS missing_order_ids,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_ids,
    COUNT(*) FILTER (WHERE order_date IS NULL) AS missing_order_dates,
    COUNT(*) FILTER (WHERE status IS NULL) AS missing_statuses,
    COUNT(*) FILTER (WHERE order_value IS NULL) AS missing_order_values,
    COUNT(*) FILTER (WHERE order_value < 0) AS negative_order_values,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_ids
FROM orders;


/*Order status breakdown*/
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM orders
GROUP BY status
ORDER BY order_count DESC;


/*Revenue and order performance*/
SELECT
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(order_value), 2) AS total_order_value,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders
WHERE status = 'Completed';


/* Monthly order trends*/
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


/*Month-over-month growth*/
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
        LAG(completed_orders) OVER (ORDER BY month) AS previous_orders,
        LAG(total_order_value) OVER (ORDER BY month) AS previous_order_value
    FROM monthly
)
SELECT
    month,
    completed_orders,
    ROUND(total_order_value, 2) AS total_order_value,
    completed_orders - previous_orders AS order_change,
    ROUND(
        100.0 * (completed_orders - previous_orders)
        / NULLIF(previous_orders, 0), 2
    ) AS order_growth_pct,
    ROUND(total_order_value - previous_order_value, 2) AS value_change,
    ROUND(
        100.0 * (total_order_value - previous_order_value)
        / NULLIF(previous_order_value, 0), 2
    ) AS value_growth_pct
FROM comparison
ORDER BY month;


/*Category-wise order performance*/
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


/*Customer-level purchase history*/
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


/*Identify potentially churned customers*/
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
    DATE '2026-10-22' - last_order_date AS days_inactive
FROM customer_activity
WHERE completed_orders >= 2
  AND DATE '2026-10-22' - last_order_date >= 45
ORDER BY days_inactive DESC;


/*Potential churn summary*/
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
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
    ) AS percentage
FROM customer_status
GROUP BY customer_status
ORDER BY customer_count DESC;


/*Check the highest-value orders*/
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


/*Verify final results*/
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(order_value), 2) AS total_order_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;