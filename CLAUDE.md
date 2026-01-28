# CLAUDE.md - OLAP Assistant Configuration

## Project Overview

**OLAP Assistant** - A natural language business intelligence system for sales analysis using a multi-agent architecture and star schema data warehouse.

---

## Dataset Documentation

### Star Schema Design

The database uses a star schema optimized for OLAP queries:

```
                     ┌──────────────┐
                     │  dim_time    │
                     │  (1,096 rows)│
                     └──────┬───────┘
                            │
    ┌──────────────┐        │        ┌──────────────┐
    │ dim_region   │        │        │ dim_product  │
    │   (5 rows)   │        │        │   (8 rows)   │
    └──────┬───────┘        │        └──────┬───────┘
           │                │               │
           └────────────────┼───────────────┘
                            │
                     ┌──────┴───────┐
                     │  fact_sales  │
                     │(10,000+ rows)│
                     └──────────────┘
```

### Fact Table: fact_sales

| Column | Type | Description |
|--------|------|-------------|
| sales_key | INTEGER | Primary key |
| transaction_id | VARCHAR(20) | Unique ID (TXN-000001 format) |
| time_key | INTEGER | Foreign key to dim_time |
| region_key | INTEGER | Foreign key to dim_region |
| product_key | INTEGER | Foreign key to dim_product |
| sales_amount | DECIMAL(12,2) | Transaction value in USD |
| quantity | INTEGER | Number of units (1-50) |
| unit_price | DECIMAL(10,2) | Price per unit |
| discount_percentage | DECIMAL(5,2) | Discount applied (0-0.20) |
| profit_margin | DECIMAL(5,2) | Profit margin (0.15-0.45) |

### Dimension Tables

**dim_time** (1,096 rows - daily for 2022-2024)
```sql
time_key        INTEGER PRIMARY KEY
full_date       DATE
day_of_week     INTEGER (0=Monday, 6=Sunday)
day_name        VARCHAR(10)
day_of_month    INTEGER
week_of_year    INTEGER
month_number    INTEGER (1-12)
month_name      VARCHAR(15)
quarter         VARCHAR(2) (Q1, Q2, Q3, Q4)
year            INTEGER (2022, 2023, 2024)
is_weekend      BOOLEAN
```

**dim_region** (5 rows)
```sql
region_key      INTEGER PRIMARY KEY
region_code     VARCHAR(10) (NORTH, SOUTH, EAST, WEST, CENTRAL)
region_name     VARCHAR(50) (North, South, East, West, Central)
```

**dim_product** (8 rows)
```sql
product_key     INTEGER PRIMARY KEY
product_code    VARCHAR(20)
product_name    VARCHAR(100)
category_key    INTEGER
category_name   VARCHAR(50) (Electronics, Computing, Accessories)
base_price      DECIMAL(10,2)
```

**dim_category** (3 rows)
```sql
category_key    INTEGER PRIMARY KEY
category_code   VARCHAR(20)
category_name   VARCHAR(50)
```

### Data Statistics

- **Total Records:** 10,000+ transactions
- **Total Sales:** ~$224 million
- **Date Range:** 2022-01-01 to 2024-12-31
- **Avg Transaction:** ~$20,400

### Dimension Hierarchies

```
TIME:     Year → Quarter → Month → Day
PRODUCT:  Category → Product
REGION:   Region (flat)
```

---

## OLAP Operations

### Supported Operations

| Operation | SQL Pattern | Description |
|-----------|------------|-------------|
| DRILL_DOWN | Add columns to GROUP BY | Navigate summary → detail |
| ROLL_UP | Remove columns from GROUP BY | Navigate detail → summary |
| SLICE | WHERE single condition | Filter one dimension |
| DICE | WHERE multiple conditions | Filter multiple dimensions |
| PIVOT | Change GROUP BY order | Rotate perspective |
| AGGREGATE | GROUP BY with SUM/AVG | Basic aggregation |

### Query Pattern

```sql
SELECT 
    <dimension_columns>,
    SUM(sales_amount) as total_sales,
    AVG(sales_amount) as avg_sales,
    COUNT(*) as count
FROM fact_sales f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_region r ON f.region_key = r.region_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE <filter_conditions>
GROUP BY <dimension_columns>
ORDER BY total_sales DESC
```

---

## Query Guidelines

### Input Format

Natural language questions about sales data.

### Output Format

```json
{
    "operation": "drill_down|roll_up|slice|dice|pivot|aggregate",
    "dimensions": ["region", "quarter", "month", "product", "category", "year"],
    "measures": ["sales_amount", "quantity", "profit_margin"],
    "filters": {"dimension": "value"},
    "explanation": "Brief description of the analysis"
}
```

### Dimension Mapping

| User Terms | Dimension | Values |
|------------|-----------|--------|
| region, area, geographic | region | North, South, East, West, Central |
| product, item | product | Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones |
| category, type | category | Electronics, Computing, Accessories |
| quarter, Q1-Q4 | quarter | Q1, Q2, Q3, Q4 |
| month, January-December | month | January through December |
| year, 2022-2024 | year | 2022, 2023, 2024 |

---

## Example Queries

### Drill-Down Examples
```
"Break down Q4 sales by region"
"Drill into North region by month"
"Show monthly details for Electronics"
"Break down 2024 by quarter"
```

### Roll-Up Examples
```
"Show total sales by category"
"Aggregate products to category level"
"Summarize by year"
"Roll up to regional totals"
```

### Slice Examples
```
"Show only Q4 sales"
"Filter to North region"
"Just 2024 data"
"Show Electronics only"
```

### Dice Examples
```
"Q4 sales in North and South"
"Compare Laptop and Phone in Q4"
"Electronics in North for 2024"
"Q4 2024 in East region"
```

### KPI Examples
```
"Year-over-year growth"
"Quarter-over-quarter performance"
"Profit margin analysis"
"Average order value"
```

---

## Agent Responsibilities

### Dimension Navigator Agent
- List available dimensions
- Show dimension hierarchies
- Suggest drill/roll paths
- Provide dimension values

### Cube Operations Agent
- Execute OLAP operations
- Build aggregation queries
- Interpret natural language
- Generate operation explanations

### KPI Calculator Agent
- Calculate growth rates (YoY, QoQ, MoM)
- Compute profit margins
- Calculate averages
- Generate interpretations

### Report Generator Agent
- Format markdown reports
- Create comparison reports
- Generate summaries
- Handle data table formatting

---

## Response Guidelines

1. **Always explain** what operation is being performed
2. **Include context** about the data being analyzed
3. **Suggest follow-ups** when appropriate
4. **Format numbers** with proper separators ($1,234.56)
5. **Use business language** that non-technical users understand

---

## Error Handling

| Error Type | Response |
|------------|----------|
| Unknown dimension | List valid options |
| Ambiguous query | Make reasonable assumption, note it |
| No data returned | Explain why, suggest alternatives |
| Invalid filter value | Show valid values |

---

## Data Generation Logic

Sales amounts are influenced by:
- **Q4 Holiday Boost:** 30% higher base sales
- **Regional Performance:** North/East +15%, Central +5%
- **Category Pricing:** Computing 2x, Electronics 1.5x multiplier
- **Random Variation:** 0.8-1.2x multiplier for realism

---

## Technical Notes

- **Database:** DuckDB (embedded OLAP database)
- **Schema Type:** Star Schema
- **Index Strategy:** Composite index on (time_key, region_key, product_key)
- **Query Limit:** 100 rows per query
- **Number Formatting:** 2 decimal places for currency
