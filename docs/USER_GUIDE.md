# User Guide

## Welcome to OLAP Assistant

This guide will help you use the OLAP Assistant to analyze your sales data using natural language queries.

---

## Getting Started

### Accessing the Application

1. Open your web browser
2. Navigate to the application URL
3. The dashboard will load with sample data automatically

### Understanding the Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Logo, Export, History, Compare, Guide, Theme Toggle    │
├───────────────────────┬─────────────────────────────────────────┤
│                       │                                         │
│   QUERY ASSISTANT     │         ANALYSIS RESULTS                │
│                       │                                         │
│   - Type queries      │   - Metric Cards (KPIs)                 │
│   - Example queries   │   - Charts (Bar, Pie, Line, Area)       │
│   - Chat history      │   - Data Tables                         │
│                       │   - Dimension Info                      │
└───────────────────────┴─────────────────────────────────────────┘
```

---

## Basic Usage

### Asking Questions

Simply type your question in natural language:

| What You Want | How to Ask |
|---------------|------------|
| Sales by region | "Show sales by region" |
| Q4 performance | "Break down Q4 sales" |
| Product comparison | "Compare Laptop vs Phone sales" |
| Monthly trend | "Show sales trend by month" |
| Category totals | "Total sales by category" |

### Using Example Queries

Click any example query to auto-fill the input:
- "Break down Q4 sales by region"
- "Show top 5 products by revenue"
- "Compare sales between North and South"
- "What's the total sales by category?"

---

## OLAP Operations Explained

### Drill-Down
Navigate from summary to detailed data.

**Example**: "Drill into North region by month"
- Starts with: North region total
- Shows: Monthly breakdown for North

### Roll-Up
Aggregate detailed data into summaries.

**Example**: "Show total sales by category"
- Starts with: Individual products
- Shows: Category totals (Electronics, Computing, Accessories)

### Slice
Filter data on a single dimension.

**Example**: "Show only Q4 sales"
- Filters: Quarter = Q4
- Shows: All Q4 data

### Dice
Filter on multiple dimensions.

**Example**: "Q4 sales in North and South regions"
- Filters: Quarter = Q4 AND Region IN (North, South)
- Shows: Filtered subset

### Pivot
Change the viewing perspective.

**Example**: "Show products as rows, quarters as columns"
- Rotates: Data view
- Shows: Different arrangement

---

## Features Guide

### 1. Chart Types

Click the "Chart Type" dropdown to switch between:

| Type | Best For |
|------|----------|
| Bar | Comparing values across categories |
| Pie | Showing proportions of a whole |
| Line | Displaying trends over time |
| Area | Showing cumulative trends |

### 2. Export Options

Click "Export" to download your data:

| Format | Use Case |
|--------|----------|
| CSV | Open in Excel, further analysis |
| Excel | Formatted spreadsheet (.xlsx) |
| PDF | Printable report with styling |

### 3. Filter Builder

Click "Filter Builder" to create filters visually:

1. Click "Add Filter"
2. Select dimension (Region, Quarter, Product)
3. Select value
4. Click "Apply Filters"

### 4. Query History

Click "History" to see past queries:

- View all queries from current session
- Click to expand and see full results
- Re-run any previous query
- Load results without re-querying

### 5. Comparison Mode

Click "Compare" for side-by-side analysis:

1. Select dimension (Region, Quarter, Product)
2. Choose first item
3. Choose second item
4. Click "Run Comparison"

### 6. Query Bookmarks

Save frequently used queries:

1. Run a query
2. Click "Save" in the header
3. Access saved queries in "Saved Queries" section

### 7. OLAP Guide

Click "OLAP Guide" to learn about operations:

- Drill-Down explanation and example
- Roll-Up explanation and example
- Slice explanation and example
- Dice explanation and example
- Pivot explanation and example

### 8. Data Cube

Click "Data Cube" to see the data structure:

- 3D visualization of dimensions
- TIME, REGION, PRODUCT axes
- Measures in the center

---

## Tips for Better Queries

### Be Specific
❌ "Show me data"
✅ "Show Q4 sales by region"

### Use Dimension Names
❌ "Break it down"
✅ "Break down by product category"

### Include Time Periods
❌ "What are sales?"
✅ "What are sales for Q4 2024?"

### Ask for Comparisons
❌ "How is North doing?"
✅ "Compare North vs South sales"

---

## Understanding Results

### Metric Cards

| Metric | Meaning |
|--------|---------|
| Total Records | Number of transactions |
| Total Sales | Sum of all sales ($) |
| Units Sold | Total quantity sold |
| Avg Sale | Average transaction value |

### Operation Badge

Click the badge (e.g., "SLICE") to learn what operation was performed.

### Dimension Badges

Click dimension names (e.g., "region") to see what each dimension represents.

### Filter Badges

Click filter badges (e.g., "quarter: Q4") to see what filters are applied.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Submit query | Enter |
| Clear input | Escape |

---

## Troubleshooting

### Query Returns No Data
- Check your filters aren't too restrictive
- Try removing some filters
- Verify dimension values are correct

### Chart Not Displaying
- Wait for query to complete
- Try switching chart types
- Refresh the page

### Export Not Working
- Ensure you have query results
- Check your browser's download settings
- Try a different export format

---

## Example Workflow

### Scenario: Quarterly Sales Analysis

1. **Start broad**: "Show total sales by quarter"
2. **Identify leader**: Note Q4 has highest sales
3. **Drill down**: "Break down Q4 by region"
4. **Find top region**: Note North leads
5. **Further detail**: "Show North Q4 sales by product"
6. **Export**: Download PDF report
7. **Save**: Bookmark the query for later

---

## Glossary

| Term | Definition |
|------|------------|
| Dimension | Category for grouping data (Region, Product, Time) |
| Measure | Numeric value to analyze (Sales, Quantity) |
| OLAP | Online Analytical Processing |
| KPI | Key Performance Indicator |
| Drill-Down | Navigate to more detail |
| Roll-Up | Aggregate to summary |
| Slice | Filter on one dimension |
| Dice | Filter on multiple dimensions |
| Pivot | Rotate the data view |

---

## Need Help?

- Click "OLAP Guide" for operation explanations
- Click any badge for more information
- Review example queries for inspiration
