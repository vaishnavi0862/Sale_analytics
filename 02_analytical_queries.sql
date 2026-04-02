-- Revenue and margin by month
SELECT
    strftime('%Y-%m', f.order_date) AS month,
    ROUND(SUM(f.quantity * f.unit_price * (1 - f.discount_pct)), 2) AS net_revenue,
    ROUND(SUM(f.quantity * (f.unit_price * (1 - f.discount_pct) - p.unit_cost)), 2) AS gross_margin
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY 1
ORDER BY 1;

-- Top products by revenue
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.quantity * f.unit_price * (1 - f.discount_pct)), 2) AS net_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY net_revenue DESC
LIMIT 10;

-- Sales by region and segment
SELECT
    c.region,
    c.segment,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.quantity * f.unit_price * (1 - f.discount_pct)), 2) AS net_revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.region, c.segment
ORDER BY net_revenue DESC;

-- Customer ranking (RFM-style: total spend)
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(DISTINCT f.order_id) AS order_count,
    ROUND(SUM(f.quantity * f.unit_price * (1 - f.discount_pct)), 2) AS lifetime_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY lifetime_value DESC;
