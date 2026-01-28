"""
DuckDB Manager for OLAP Assistant.
Implements a Star Schema for OLAP analytics with 10,000+ transactions.
"""

import duckdb
import os
import random
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Data configuration
REGIONS = ["North", "South", "East", "West", "Central"]
PRODUCTS = [
    ("LAPTOP", "Laptop", "Computing", 999.99),
    ("DESKTOP", "Desktop", "Computing", 799.99),
    ("TABLET", "Tablet", "Computing", 499.99),
    ("PHONE", "Phone", "Electronics", 699.99),
    ("MONITOR", "Monitor", "Electronics", 299.99),
    ("KEYBOARD", "Keyboard", "Accessories", 79.99),
    ("MOUSE", "Mouse", "Accessories", 49.99),
    ("HEADPHONES", "Headphones", "Accessories", 149.99),
]
CATEGORIES = ["Electronics", "Computing", "Accessories"]
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


class DuckDBManager:
    """
    Manages DuckDB database operations with Star Schema design.
    
    Star Schema:
    - Fact Table: fact_sales (transactions)
    - Dimension Tables: dim_time, dim_region, dim_product, dim_category
    """
    
    def __init__(self, db_path: str = None):
        """Initialize the DuckDB manager."""
        if db_path is None:
            # Use a file in the data directory for persistence
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "olap_warehouse.duckdb")
        
        self.db_path = db_path
        self._conn = None
        self._initialized = False
    
    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = duckdb.connect(self.db_path)
        return self._conn
    
    def initialize_schema(self):
        """Create the star schema tables if they don't exist."""
        if self._initialized:
            return
        
        logger.info("Initializing DuckDB star schema...")
        
        # Create dimension tables
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_time (
                time_key INTEGER PRIMARY KEY,
                full_date DATE NOT NULL,
                day_of_week INTEGER NOT NULL,
                day_name VARCHAR(10) NOT NULL,
                day_of_month INTEGER NOT NULL,
                week_of_year INTEGER NOT NULL,
                month_number INTEGER NOT NULL,
                month_name VARCHAR(15) NOT NULL,
                quarter VARCHAR(2) NOT NULL,
                year INTEGER NOT NULL,
                is_weekend BOOLEAN NOT NULL
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_region (
                region_key INTEGER PRIMARY KEY,
                region_code VARCHAR(10) NOT NULL,
                region_name VARCHAR(50) NOT NULL
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_category (
                category_key INTEGER PRIMARY KEY,
                category_code VARCHAR(20) NOT NULL,
                category_name VARCHAR(50) NOT NULL
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_product (
                product_key INTEGER PRIMARY KEY,
                product_code VARCHAR(20) NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                category_key INTEGER REFERENCES dim_category(category_key),
                category_name VARCHAR(50) NOT NULL,
                base_price DECIMAL(10,2)
            )
        """)
        
        # Create fact table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                sales_key INTEGER PRIMARY KEY,
                transaction_id VARCHAR(20) NOT NULL,
                time_key INTEGER REFERENCES dim_time(time_key),
                region_key INTEGER REFERENCES dim_region(region_key),
                product_key INTEGER REFERENCES dim_product(product_key),
                sales_amount DECIMAL(12,2) NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                discount_percentage DECIMAL(5,2) DEFAULT 0,
                profit_margin DECIMAL(5,2) NOT NULL
            )
        """)
        
        # Create indexes for OLAP queries
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_fact_time ON fact_sales(time_key)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_fact_region ON fact_sales(region_key)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_sales(product_key)")
        
        self._initialized = True
        logger.info("Schema initialized successfully")
    
    def populate_dimensions(self):
        """Populate dimension tables with reference data."""
        # Check if already populated
        count = self.conn.execute("SELECT COUNT(*) FROM dim_region").fetchone()[0]
        if count > 0:
            logger.info("Dimensions already populated")
            return
        
        logger.info("Populating dimension tables...")
        
        # Populate regions
        for idx, region in enumerate(REGIONS, 1):
            self.conn.execute(
                "INSERT INTO dim_region VALUES (?, ?, ?)",
                [idx, region.upper(), region]
            )
        
        # Populate categories
        for idx, category in enumerate(CATEGORIES, 1):
            self.conn.execute(
                "INSERT INTO dim_category VALUES (?, ?, ?)",
                [idx, category[:4].upper(), category]
            )
        
        # Populate products
        category_map = {c: idx for idx, c in enumerate(CATEGORIES, 1)}
        for idx, (code, name, category, price) in enumerate(PRODUCTS, 1):
            self.conn.execute(
                "INSERT INTO dim_product VALUES (?, ?, ?, ?, ?, ?)",
                [idx, code, name, category_map[category], category, price]
            )
        
        # Populate time dimension for 2022-2024
        time_key = 1
        for year in [2022, 2023, 2024]:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            current_date = start_date
            
            while current_date <= end_date:
                day_of_week = current_date.weekday()
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                quarter = f"Q{(current_date.month - 1) // 3 + 1}"
                
                self.conn.execute(
                    "INSERT INTO dim_time VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [
                        time_key,
                        current_date,
                        day_of_week,
                        day_names[day_of_week],
                        current_date.day,
                        current_date.isocalendar()[1],
                        current_date.month,
                        MONTHS[current_date.month - 1],
                        quarter,
                        year,
                        day_of_week >= 5  # is_weekend
                    ]
                )
                time_key += 1
                current_date += timedelta(days=1)
        
        logger.info(f"Populated dimensions: {time_key - 1} time records")
    
    def generate_sales_data(self, target_count: int = 10500) -> int:
        """Generate sales fact data to reach target count."""
        current_count = self.conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        
        if current_count >= target_count:
            logger.info(f"Sales data already has {current_count} records")
            return current_count
        
        # Clear existing data if below target
        if current_count > 0:
            logger.info(f"Clearing existing {current_count} records to regenerate...")
            self.conn.execute("DELETE FROM fact_sales")
        
        logger.info(f"Generating {target_count}+ sales records...")
        
        # Get dimension keys
        time_keys = self.conn.execute(
            "SELECT time_key, quarter, month_number, year FROM dim_time"
        ).fetchall()
        region_keys = self.conn.execute("SELECT region_key, region_name FROM dim_region").fetchall()
        product_keys = self.conn.execute(
            "SELECT product_key, product_name, category_name, base_price FROM dim_product"
        ).fetchall()
        
        sales_key = 1
        batch_data = []
        
        # Generate transactions distributed across time, regions, and products
        for time_key, quarter, month, year in time_keys:
            # Not every day has transactions - sample ~30% of days
            if random.random() > 0.3:
                continue
            
            for region_key, region_name in region_keys:
                # Each region has 0-3 transactions per active day
                num_txns = random.randint(0, 3)
                
                for _ in range(num_txns):
                    # Select a random product
                    product_key, product_name, category, base_price = random.choice(product_keys)
                    
                    # Convert base_price to float if it's Decimal
                    base_price_float = float(base_price) if base_price else 100.0
                    
                    # Calculate sales with realistic variations
                    quantity = random.randint(1, 50)
                    
                    # Price variation based on factors
                    price_multiplier = 1.0
                    
                    # Q4 holiday boost
                    if quarter == "Q4":
                        price_multiplier *= 1.3
                    
                    # Regional performance
                    if region_name in ["North", "East"]:
                        price_multiplier *= 1.15
                    elif region_name == "Central":
                        price_multiplier *= 1.05
                    
                    # Product category pricing
                    if category == "Computing":
                        price_multiplier *= 2.0
                    elif category == "Electronics":
                        price_multiplier *= 1.5
                    
                    unit_price = round(base_price_float * price_multiplier * random.uniform(0.8, 1.2), 2)
                    sales_amount = round(unit_price * quantity, 2)
                    discount = round(random.uniform(0, 0.20), 2)
                    profit_margin = round(random.uniform(0.15, 0.45), 2)
                    
                    batch_data.append((
                        sales_key,
                        f"TXN-{sales_key:06d}",
                        time_key,
                        region_key,
                        product_key,
                        sales_amount,
                        quantity,
                        unit_price,
                        discount,
                        profit_margin
                    ))
                    sales_key += 1
                    
                    # Batch insert every 1000 records
                    if len(batch_data) >= 1000:
                        self.conn.executemany(
                            "INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            batch_data
                        )
                        batch_data = []
        
        # Insert remaining batch
        if batch_data:
            self.conn.executemany(
                "INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                batch_data
            )
        
        # If we didn't reach target, generate more transactions
        current_count = self.conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        
        while current_count < target_count:
            additional_needed = target_count - current_count + 500  # Buffer
            batch_data = []
            
            for _ in range(additional_needed):
                time_key = random.choice(time_keys)[0]
                region_key = random.choice(region_keys)[0]
                product_key, product_name, category, base_price = random.choice(product_keys)
                
                # Convert base_price to float if it's Decimal
                base_price_float = float(base_price) if base_price else 100.0
                
                quantity = random.randint(1, 50)
                unit_price = round(base_price_float * random.uniform(1.0, 2.5), 2)
                sales_amount = round(unit_price * quantity, 2)
                
                batch_data.append((
                    sales_key,
                    f"TXN-{sales_key:06d}",
                    time_key,
                    region_key,
                    product_key,
                    sales_amount,
                    quantity,
                    unit_price,
                    round(random.uniform(0, 0.20), 2),
                    round(random.uniform(0.15, 0.45), 2)
                ))
                sales_key += 1
            
            self.conn.executemany(
                "INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                batch_data
            )
            current_count = self.conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        
        final_count = self.conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        logger.info(f"Generated {final_count} sales records")
        return final_count
    
    def initialize_all(self) -> int:
        """Initialize schema, populate dimensions, and generate data."""
        self.initialize_schema()
        self.populate_dimensions()
        return self.generate_sales_data()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the data warehouse."""
        result = self.conn.execute("""
            SELECT 
                COUNT(*) as total_records,
                COALESCE(SUM(sales_amount), 0) as total_sales,
                COALESCE(SUM(quantity), 0) as total_quantity,
                COALESCE(AVG(sales_amount), 0) as avg_sale
            FROM fact_sales
        """).fetchone()
        
        regions = [r[0] for r in self.conn.execute(
            "SELECT region_name FROM dim_region ORDER BY region_name"
        ).fetchall()]
        
        products = [r[0] for r in self.conn.execute(
            "SELECT product_name FROM dim_product ORDER BY product_name"
        ).fetchall()]
        
        quarters = [r[0] for r in self.conn.execute(
            "SELECT DISTINCT quarter FROM dim_time ORDER BY quarter"
        ).fetchall()]
        
        years = [r[0] for r in self.conn.execute(
            "SELECT DISTINCT year FROM dim_time ORDER BY year"
        ).fetchall()]
        
        return {
            "total_records": result[0],
            "total_sales": round(result[1], 2),
            "total_quantity": result[2],
            "avg_sale": round(result[3], 2),
            "dimensions": {
                "regions": regions,
                "products": products,
                "quarters": quarters,
                "years": years
            }
        }
    
    def execute_olap_query(
        self,
        dimensions: List[str],
        measures: List[str],
        filters: Dict[str, Any] = None,
        operation: str = "aggregate"
    ) -> Dict[str, Any]:
        """Execute an OLAP query on the star schema."""
        
        # Map user dimension names to actual columns
        dim_mapping = {
            "region": "r.region_name",
            "product": "p.product_name",
            "category": "p.category_name",
            "quarter": "t.quarter",
            "month": "t.month_name",
            "year": "t.year"
        }
        
        # Build SELECT clause
        select_dims = []
        group_dims = []
        for dim in dimensions:
            if dim.lower() in dim_mapping:
                col = dim_mapping[dim.lower()]
                select_dims.append(f"{col} as {dim.lower()}")
                group_dims.append(col)
        
        # Build measure aggregations
        measure_aggs = []
        for measure in measures:
            if measure in ["sales_amount", "quantity", "profit_margin", "unit_price"]:
                measure_aggs.append(f"SUM(f.{measure}) as total_{measure}")
                measure_aggs.append(f"AVG(f.{measure}) as avg_{measure}")
        
        measure_aggs.append("COUNT(*) as count")
        
        # Build WHERE clause
        where_clauses = []
        params = []
        if filters:
            for key, value in filters.items():
                if key.lower() == "region":
                    where_clauses.append("r.region_name = ?")
                    params.append(value)
                elif key.lower() == "quarter":
                    where_clauses.append("t.quarter = ?")
                    params.append(value)
                elif key.lower() == "year":
                    where_clauses.append("t.year = ?")
                    params.append(int(value) if isinstance(value, str) else value)
                elif key.lower() == "month":
                    where_clauses.append("t.month_name = ?")
                    params.append(value)
                elif key.lower() == "product":
                    where_clauses.append("p.product_name = ?")
                    params.append(value)
                elif key.lower() == "category":
                    where_clauses.append("p.category_name = ?")
                    params.append(value)
        
        # Build the full query - handle case when no dimensions specified
        if not select_dims:
            # Default to region if no dimensions
            select_dims = ["r.region_name as region"]
            group_dims = ["r.region_name"]
        
        # Determine ORDER BY column - use first aggregate or count
        order_col = "total_sales_amount" if "SUM(f.sales_amount) as total_sales_amount" in measure_aggs else "count"
        
        query = f"""
            SELECT {', '.join(select_dims + measure_aggs)}
            FROM fact_sales f
            JOIN dim_time t ON f.time_key = t.time_key
            JOIN dim_region r ON f.region_key = r.region_key
            JOIN dim_product p ON f.product_key = p.product_key
            {'WHERE ' + ' AND '.join(where_clauses) if where_clauses else ''}
            GROUP BY {', '.join(group_dims)}
            ORDER BY {order_col} DESC
            LIMIT 100
        """
        
        # Execute query
        result = self.conn.execute(query, params).fetchall()
        columns = [desc[0] for desc in self.conn.description]
        
        # Format results
        data = []
        for row in result:
            record = {}
            for i, col in enumerate(columns):
                val = row[i]
                if isinstance(val, float):
                    record[col] = round(val, 2)
                else:
                    record[col] = val
            data.append(record)
        
        return {
            "operation": operation,
            "dimensions": dimensions,
            "measures": measures,
            "filters": filters or {},
            "data": data,
            "row_count": len(data)
        }
    
    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


# Singleton instance
db_manager = DuckDBManager()
