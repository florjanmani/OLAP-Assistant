-- =============================================================================
-- OLAP ASSISTANT - STAR SCHEMA DATABASE DESIGN
-- =============================================================================
-- This schema implements a star schema for OLAP analysis
-- Designed for: Sales Analytics with 10,000+ transactions
-- =============================================================================

-- =============================================================================
-- DIMENSION TABLES
-- =============================================================================

-- Time Dimension (Type 1 SCD)
CREATE TABLE dim_time (
    time_key SERIAL PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_year INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    quarter VARCHAR(2) NOT NULL,
    year INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    fiscal_quarter VARCHAR(6),
    fiscal_year INTEGER
);

-- Geography/Region Dimension
CREATE TABLE dim_region (
    region_key SERIAL PRIMARY KEY,
    region_code VARCHAR(10) NOT NULL UNIQUE,
    region_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) DEFAULT 'USA',
    timezone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- Product Dimension
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_code VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    category_key INTEGER,
    category_name VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    expiry_date DATE
);

-- Category Dimension (for roll-up)
CREATE TABLE dim_category (
    category_key SERIAL PRIMARY KEY,
    category_code VARCHAR(20) NOT NULL UNIQUE,
    category_name VARCHAR(50) NOT NULL,
    parent_category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================================================================
-- FACT TABLE
-- =============================================================================

-- Sales Fact Table
CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    transaction_id VARCHAR(20) NOT NULL UNIQUE,
    
    -- Foreign Keys to Dimensions
    time_key INTEGER REFERENCES dim_time(time_key),
    region_key INTEGER REFERENCES dim_region(region_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    
    -- Measures (Facts)
    sales_amount DECIMAL(12,2) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    net_sales DECIMAL(12,2),
    profit_margin DECIMAL(5,2),
    profit_amount DECIMAL(12,2),
    
    -- Audit Fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- INDEXES FOR OLAP QUERIES
-- =============================================================================

-- Time dimension indexes
CREATE INDEX idx_time_year ON dim_time(year);
CREATE INDEX idx_time_quarter ON dim_time(quarter);
CREATE INDEX idx_time_month ON dim_time(month_number);
CREATE INDEX idx_time_date ON dim_time(full_date);

-- Region dimension indexes
CREATE INDEX idx_region_name ON dim_region(region_name);

-- Product dimension indexes
CREATE INDEX idx_product_category ON dim_product(category_name);
CREATE INDEX idx_product_name ON dim_product(product_name);

-- Fact table indexes (for common OLAP queries)
CREATE INDEX idx_fact_time ON fact_sales(time_key);
CREATE INDEX idx_fact_region ON fact_sales(region_key);
CREATE INDEX idx_fact_product ON fact_sales(product_key);
CREATE INDEX idx_fact_composite ON fact_sales(time_key, region_key, product_key);

-- =============================================================================
-- VIEWS FOR COMMON OLAP QUERIES
-- =============================================================================

-- Denormalized view for easier querying
CREATE VIEW vw_sales_analysis AS
SELECT 
    f.transaction_id,
    t.full_date,
    t.month_name,
    t.quarter,
    t.year,
    r.region_name,
    p.product_name,
    p.category_name,
    f.sales_amount,
    f.quantity,
    f.unit_price,
    f.profit_margin,
    f.net_sales
FROM fact_sales f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_region r ON f.region_key = r.region_key
JOIN dim_product p ON f.product_key = p.product_key;

-- Aggregated view by region and quarter
CREATE VIEW vw_regional_quarterly_sales AS
SELECT 
    t.year,
    t.quarter,
    r.region_name,
    SUM(f.sales_amount) as total_sales,
    SUM(f.quantity) as total_quantity,
    AVG(f.profit_margin) as avg_margin,
    COUNT(*) as transaction_count
FROM fact_sales f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_region r ON f.region_key = r.region_key
GROUP BY t.year, t.quarter, r.region_name;

-- Aggregated view by product category
CREATE VIEW vw_category_sales AS
SELECT 
    p.category_name,
    t.year,
    SUM(f.sales_amount) as total_sales,
    SUM(f.quantity) as total_quantity,
    COUNT(DISTINCT p.product_key) as product_count
FROM fact_sales f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category_name, t.year;

-- =============================================================================
-- SAMPLE DATA INSERTION (Dimension Tables)
-- =============================================================================

-- Insert regions
INSERT INTO dim_region (region_code, region_name) VALUES
('NORTH', 'North'),
('SOUTH', 'South'),
('EAST', 'East'),
('WEST', 'West'),
('CENTRAL', 'Central');

-- Insert categories
INSERT INTO dim_category (category_code, category_name) VALUES
('ELEC', 'Electronics'),
('COMP', 'Computing'),
('ACCS', 'Accessories');

-- Insert products
INSERT INTO dim_product (product_code, product_name, category_name, unit_price) VALUES
('LAPTOP', 'Laptop', 'Computing', 999.99),
('DESKTOP', 'Desktop', 'Computing', 799.99),
('TABLET', 'Tablet', 'Computing', 499.99),
('PHONE', 'Phone', 'Electronics', 699.99),
('MONITOR', 'Monitor', 'Electronics', 299.99),
('KEYBOARD', 'Keyboard', 'Accessories', 79.99),
('MOUSE', 'Mouse', 'Accessories', 49.99),
('HEADPHONES', 'Headphones', 'Accessories', 149.99);

-- =============================================================================
-- COMMENTS
-- =============================================================================

COMMENT ON TABLE fact_sales IS 'Central fact table containing all sales transactions';
COMMENT ON TABLE dim_time IS 'Time dimension for temporal analysis';
COMMENT ON TABLE dim_region IS 'Geographic dimension for regional analysis';
COMMENT ON TABLE dim_product IS 'Product dimension with category hierarchy';
COMMENT ON VIEW vw_sales_analysis IS 'Denormalized view for OLAP queries';
