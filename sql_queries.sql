USE ecommerce_dw;


-- 1. Total sales and revenue

SELECT
    COUNT(*) AS total_sales,
    SUM(revenue) AS total_revenue
FROM fact_sales;


-- 2. Top 10 products by revenue

SELECT
    p.description,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.stock_code = p.stock_code
GROUP BY
    p.stock_code,
    p.description
ORDER BY revenue DESC
LIMIT 10;


-- 3. Revenue by country

SELECT
    c.country,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Monthly revenue

SELECT
    d.year,
    d.month,
    SUM(f.revenue) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month
ORDER BY
    d.year,
    d.month;


-- 5. Top 10 customers by revenue

SELECT
    f.customer_id,
    SUM(f.revenue) AS customer_revenue
FROM fact_sales f
GROUP BY f.customer_id
ORDER BY customer_revenue DESC
LIMIT 10;


-- 6. Average order value

SELECT
    AVG(order_total) AS average_order_value
FROM (
    SELECT
        invoice_no,
        SUM(revenue) AS order_total
    FROM fact_sales
    GROUP BY invoice_no
) orders;


-- 7. Revenue by year

SELECT
    d.year,
    SUM(f.revenue) AS yearly_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;

-- =====================================================
-- Analytical View: Monthly Revenue
-- =====================================================

CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    d.year,
    d.month,
    SUM(f.revenue) AS total_revenue,
    COUNT(*) AS total_transactions
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month;