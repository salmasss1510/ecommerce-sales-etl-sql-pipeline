
-- Create the database
CREATE DATABASE IF NOT EXISTS ecommerce_dw;

USE ecommerce_dw;

-- 1. Customer dimension
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    country VARCHAR(100)
);

-- 2. Product dimension
CREATE TABLE IF NOT EXISTS dim_product (
    stock_code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255)
);

-- 3. Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

-- 4. Central sales fact table
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no VARCHAR(20),
    stock_code VARCHAR(20),
    customer_id VARCHAR(20),
    date_key DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    revenue DECIMAL(12,2),

    FOREIGN KEY (stock_code)
        REFERENCES dim_product(stock_code),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);
