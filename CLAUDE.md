# CLAUDE.md - OLAP Assistant Configuration

## Project Overview
OLAP Assistant - Natural language business intelligence system for sales analysis.

## Dataset Documentation

### Schema
```
sales_data {
    transaction_id: string (TXN-000001)
    region: string [North, South, East, West, Central]
    product: string [Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones]
    category: string [Electronics, Computing, Accessories]
    sales_amount: float (500 - 50000)
    quantity: int (1 - 50)
    unit_price: float
    quarter: string [Q1, Q2, Q3, Q4]
    month: string [January - December]
    year: int [2022, 2023, 2024]
    profit_margin: float (0.15 - 0.45)
    discount: float (0 - 0.20)
}
```

### Record Count: 10,000+ transactions

### Dimension Hierarchies
- Time: Year → Quarter → Month → Day
- Product: Category → Product
- Geography: Region

## OLAP Operations

### Supported Operations
1. **DRILL_DOWN** - Navigate from summary to detail
2. **ROLL_UP** - Aggregate from detail to summary
3. **SLICE** - Filter on single dimension
4. **DICE** - Filter on multiple dimensions
5. **PIVOT** - Rotate the data view

## Query Guidelines

### Input Format
Natural language questions about sales data.

### Output Format
```json
{
    "operation": "drill_down|roll_up|slice|dice|pivot|aggregate",
    "dimensions": ["list of dimensions to group by"],
    "measures": ["sales_amount", "quantity"],
    "filters": {"dimension": "value"},
    "explanation": "Brief explanation"
}
```

## Example Queries

### Drill-Down
- "Break down Q4 sales by region"
- "Drill into North region by month"
- "Show monthly details for Electronics"

### Roll-Up
- "Show total sales by category"
- "Aggregate products to category level"
- "Summarize by year"

### Slice
- "Show only Q4 sales"
- "Filter to North region"
- "Just 2024 data"

### Dice
- "Q4 sales in North and South"
- "Compare Laptop and Phone in Q4"
- "Electronics in North for 2024"

### KPI
- "Year-over-year growth"
- "Quarter-over-quarter performance"
- "Profit margin analysis"

## Agent Responsibilities

### Dimension Navigator
- List available dimensions
- Show hierarchies
- Suggest drill paths

### Cube Operations
- Execute OLAP operations
- Build aggregation queries
- Interpret natural language

### KPI Calculator
- Calculate growth rates
- Compute margins
- Generate summaries

### Report Generator
- Format reports
- Create summaries
- Handle exports

## Response Guidelines

1. Always explain what operation is being performed
2. Include relevant context about the data
3. Suggest follow-up analyses
4. Format numbers with proper separators
5. Use clear, business-friendly language

## Error Handling

- Unknown dimension → Suggest valid options
- Ambiguous query → Make reasonable assumption, note it
- No data → Explain why, suggest alternatives
