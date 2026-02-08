-- Assumed table: orders
-- Columns:
-- order_id, user_id, product_id, quantity,
-- order_date, ingestion_date, order_year, order_month


-- 1. Total order rows (order-line level)
SELECT COUNT(*) AS total_rows
FROM orders;


-- 2. Total unique orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- 3. Total unique users
SELECT COUNT(DISTINCT user_id) AS total_users
FROM orders;


-- 4. Total unique products
SELECT COUNT(DISTINCT product_id) AS total_products
FROM orders;


-- 5. Orders per user
SELECT
    user_id,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY user_id
ORDER BY total_orders DESC;


-- 6. Users with repeat orders
SELECT
    user_id,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY user_id
HAVING COUNT(DISTINCT order_id) > 1;


-- 7. Total quantity sold per product
SELECT
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
GROUP BY product_id
ORDER BY total_quantity DESC;


-- 8. Top 10 selling products
SELECT
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
GROUP BY product_id
ORDER BY total_quantity DESC
LIMIT 10;


-- 9. Number of products per order
SELECT
    order_id,
    COUNT(DISTINCT product_id) AS products_count
FROM orders
GROUP BY order_id
ORDER BY products_count DESC;


-- 10. Average items per order
SELECT AVG(items_per_order) AS avg_items_per_order
FROM (
    SELECT
        order_id,
        SUM(quantity) AS items_per_order
    FROM orders
    GROUP BY order_id
) t;


-- 11. Orders per day
SELECT
    order_date,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- 12. Orders per month
SELECT
    order_year,
    order_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;


-- 13. Monthly order trend
SELECT
    order_year,
    order_month,
    COUNT(*) AS order_rows
FROM orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;


-- 14. Null check on key columns
SELECT
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS null_user_id,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id
FROM orders;


-- 15. Duplicate order-product records
SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;


-- 16. Total items purchased per user
SELECT
    user_id,
    SUM(quantity) AS total_items
FROM orders
GROUP BY user_id
ORDER BY total_items DESC;


-- 17. Orders with highest total quantity
SELECT
    order_id,
    SUM(quantity) AS total_items
FROM orders
GROUP BY order_id
ORDER BY total_items DESC;


-- 18. Orders ingested today
SELECT COUNT(*) AS today_rows
FROM orders
WHERE ingestion_date = CURRENT_DATE;


-- 19. First and last order date
SELECT
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders;


-- 20. User–product purchase matrix
SELECT
    user_id,
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
GROUP BY user_id, product_id
ORDER BY user_id, total_quantity DESC;
