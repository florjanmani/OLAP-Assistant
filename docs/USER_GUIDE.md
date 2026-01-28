# OLAP Assistant - User Guide

## Introduction

Welcome to the OLAP Assistant! This guide will help you use the application to analyze sales data using natural language queries.

---

## What is OLAP?

**OLAP (Online Analytical Processing)** is a technology that allows you to analyze data from multiple perspectives. Think of your data as a cube with different dimensions:

```
                    ┌───────────────┐
                   /               /│
                  /   TIME        / │
                 /               /  │
                ┌───────────────┐   │
                │               │   │
    REGION ──── │   SALES DATA  │ ──── PRODUCT
                │               │   │
                │               │  /
                └───────────────┘ /
                                 /
```

**Dimensions** are categories you can group by:
- **Time**: Year, Quarter, Month
- **Region**: North, South, East, West, Central
- **Product**: Laptop, Phone, Tablet, etc.

**Measures** are the numbers you analyze:
- Sales Amount ($)
- Quantity Sold
- Profit Margin

---

## Getting Started

### Dashboard Overview

When you open the application, you'll see:

1. **Metric Cards** (top) - Summary statistics
   - Total Records: Number of transactions
   - Total Sales: Sum of all sales
   - Units Sold: Total quantity
   - Avg Sale: Average transaction value

2. **Query Assistant** (left panel) - Where you type questions

3. **Analysis Results** (center) - Charts and tables

4. **Available Dimensions** (bottom) - Data exploration options

---

## Asking Questions

Type your question in natural language. Here are examples for each OLAP operation:

### Drill-Down (See More Detail)

Go from summary to detail level.

```
"Break down Q4 sales by month"
"Drill into North region by product"
"Show monthly details for 2024"
```

### Roll-Up (See Summary)

Aggregate from detail to summary.

```
"Show total sales by category"
"What's the overall sales by year?"
"Summarize products to category level"
```

### Slice (Filter One Thing)

Filter on a single dimension.

```
"Show only Q4 sales"
"Filter to North region"
"Just 2024 data"
```

### Dice (Filter Multiple Things)

Filter on multiple dimensions at once.

```
"Q4 sales in North and South regions"
"Compare Laptop and Phone in Q4"
"Electronics in North for 2024"
```

### Pivot (Change Perspective)

See data from a different angle.

```
"Show products by region instead of region by products"
"Pivot quarters as columns"
```

---

## Using the Interface

### Filter Builder

Click **"Filter Builder"** to visually create filters:

1. Click "Add Filter"
2. Select a dimension (Region, Quarter, Year, Product)
3. Select a value
4. Repeat for multiple filters
5. Click "Apply Filters"

### OLAP Guide

Click **"OLAP Guide"** to see explanations of all operations with examples. Click any "Try:" link to populate a sample query.

### Data Cube

Click **"Data Cube"** to see a visual representation of how your data is organized in a multidimensional cube.

### Query History

Click **"History"** to see all your previous queries. You can:
- Click to expand and see full results
- Click "Re-run Query" to run it again
- Click "Load Results" to view past results

### Comparison Mode

Click **"Compare"** to compare two items side-by-side:

1. Select what to compare by (Region, Quarter, Product)
2. Select first item
3. Select second item
4. Click "Run Comparison"

---

## Understanding Results

### Charts

The analysis results appear as charts. Use the chart type selector:

- **Bar Chart**: Compare values across categories
- **Pie Chart**: See proportions of a whole
- **Line Chart**: View trends over time
- **Area Chart**: See cumulative values

### Data Table

Click "Table" tab to see the raw numbers:

| Region | Total Sales | Avg Sales | Count |
|--------|-------------|-----------|-------|
| North  | $47.8M      | $21,168   | 2,259 |
| East   | $45.9M      | $20,882   | 2,198 |
| ...    | ...         | ...       | ...   |

### OLAP Operation Badge

Each result shows a colored badge indicating the operation:
- 🔵 **DRILL-DOWN** - Blue
- 🟢 **ROLL-UP** - Green
- 🟣 **SLICE** - Purple
- 🟠 **DICE** - Orange
- 🔴 **PIVOT** - Pink
- 🔷 **AGGREGATE** - Cyan

Click the badge to learn more about that operation.

---

## Exporting Results

Click **"Export"** to download your analysis:

| Format | Best For |
|--------|----------|
| **CSV** | Spreadsheet software (Excel, Google Sheets) |
| **Excel** | Native Excel with formatting |
| **PDF Report** | Sharing with colleagues, presentations |

---

## Saving Queries

### Bookmarks

Click **"Save"** button to bookmark a query. Your saved queries appear in the left panel and persist between sessions.

### History

All queries are automatically saved in history. Access via the "History" button.

---

## Tips for Better Queries

### Be Specific

❌ "Show me sales"  
✅ "Show Q4 2024 sales by region"

### Use Dimension Names

❌ "Break it down more"  
✅ "Break down by month"

### Combine Operations

✅ "Show Q4 sales by region, then drill into North by month"

### Ask Follow-ups

After seeing results, ask related questions:
1. "Show sales by region"
2. "Drill into North by quarter"
3. "Compare Q3 and Q4 for North"

---

## Example Analysis Session

Here's a typical analysis workflow:

**Step 1: Get Overview**
```
Query: "What are total sales by region?"
Result: See which regions perform best
```

**Step 2: Investigate Top Performer**
```
Query: "Drill into North region by quarter"
Result: See seasonal patterns
```

**Step 3: Focus on Peak Period**
```
Query: "Show North Q4 sales by product"
Result: See which products drove Q4 success
```

**Step 4: Compare**
```
Query: "Compare Laptop and Phone sales in North Q4"
Result: Side-by-side product comparison
```

**Step 5: Export**
```
Click Export → PDF to share findings
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send query |
| `↑` | Previous query (when input focused) |
| `Escape` | Close dialogs |

---

## Dark Mode

Click the moon/sun icon in the header to toggle between light and dark themes.

---

## Troubleshooting

### "No Analysis Yet"

The analysis panel is empty until you ask a question. Type a query and press Enter or click the send button.

### Query Doesn't Work

Try rephrasing:
- Be more specific about dimensions
- Use exact names (e.g., "Q4" not "fourth quarter")
- Check spelling of regions and products

### Chart Not Showing

- Ensure your query returned data (check row count)
- Switch to Table view to see raw results
- Try a broader query (fewer filters)

---

## Glossary

| Term | Definition |
|------|------------|
| **Dimension** | A category to group data by (Region, Time, Product) |
| **Measure** | A numeric value to analyze (Sales, Quantity) |
| **Drill-Down** | Go from summary to detail (Year → Month) |
| **Roll-Up** | Go from detail to summary (Product → Category) |
| **Slice** | Filter on one dimension (only Q4) |
| **Dice** | Filter on multiple dimensions (Q4 AND North) |
| **Pivot** | Rotate the view of data |
| **Star Schema** | Database design with fact and dimension tables |
| **Fact Table** | Contains transaction records |
| **Dimension Table** | Contains reference data (regions, products) |

---

## Getting Help

If you have questions about:
- **OLAP Concepts**: Click "OLAP Guide" in the header
- **Data Structure**: Click "Data Cube" to visualize
- **Query Syntax**: See example queries in the left panel
- **Technical Issues**: Contact the system administrator

---

**Happy Analyzing!** 📊
