# OLAP Assistant - Project Documentation
## Kurs Special ne Informatike - School Project

---

## 📋 WHAT IS THIS PROJECT?

This is an **OLAP Assistant** - a web application that allows business users to analyze sales data using **natural language** instead of writing SQL queries. 

**Example:** Instead of writing complex SQL like:
```sql
SELECT region, SUM(sales_amount) FROM sales WHERE quarter = 'Q4' GROUP BY region
```

Users simply type:
```
"Break down Q4 sales by region"
```

The system understands the request and executes the appropriate OLAP operation.

---

## 🎯 WHAT IS OLAP?

**OLAP = Online Analytical Processing**

OLAP is a technology for analyzing multidimensional data from multiple perspectives. Think of it as a "data cube" where:

- **Dimensions** = Categories to group data by (Region, Product, Time)
- **Measures** = Numbers to calculate (Sales Amount, Quantity)
- **Facts** = The actual data records

### The 5 OLAP Operations:

| Operation | What it Does | Example |
|-----------|--------------|---------|
| **Drill-Down** | Go from summary → detail | Year → Quarter → Month |
| **Roll-Up** | Go from detail → summary | Product → Category |
| **Slice** | Filter on ONE dimension | Only show Q4 data |
| **Dice** | Filter on MULTIPLE dimensions | Q4 AND North region |
| **Pivot** | Rotate the view | Swap rows and columns |

---

## 📊 THE DATASET

The application uses **sample sales data** with **960 records**.

### Data Structure:

| Field | Description | Values |
|-------|-------------|--------|
| `region` | Geographic area | North, South, East, West, Central |
| `product` | Item sold | Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones |
| `category` | Product group | Electronics, Computing, Accessories |
| `sales_amount` | Sale value ($) | $5,000 - $65,000 per record |
| `quantity` | Units sold | 10 - 200 units |
| `quarter` | Fiscal quarter | Q1, Q2, Q3, Q4 |
| `month` | Calendar month | January - December |
| `year` | Year | 2023, 2024 |

### Data Summary:
- **Total Records:** 960
- **Total Sales:** $28,821,495.98
- **Total Units Sold:** 103,172
- **Average Sale:** $30,022.39
- **Date Range:** 2023 - 2024

### Data Generation Logic:
- Q4 has **30% higher sales** (holiday season simulation)
- North and East regions have **15% higher sales** (regional variation)
- Each month has records for all 5 regions × 8 products

---

## 🛠️ TECHNOLOGY STACK

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React.js + Tailwind CSS | User interface |
| **Backend** | FastAPI (Python) | API server |
| **Database** | MongoDB | Data storage |
| **Charts** | Recharts | Data visualization |

---

## ✨ FEATURES BUILT

### Core Features:
1. **Natural Language Queries** - Ask questions in plain English
2. **Query Processing** - System understands and executes OLAP operations
3. **Data Visualization** - Bar, Pie, Line, Area charts
4. **Data Tables** - Formatted results with all metrics

### Export Options:
5. **CSV Export** - Download data as spreadsheet
6. **Excel Export** - Download as .xlsx file
7. **PDF Report** - Professional formatted report

### Interactive Features:
8. **Query Bookmarking** - Save favorite queries
9. **Query History** - View all past queries with full results
10. **Comparison Mode** - Compare two regions/products side-by-side
11. **Filter Builder** - Visual filter creation without typing

### Educational Features:
12. **OLAP Operations Guide** - Explains all 5 operations with examples
13. **Data Cube Visualization** - 3D diagram showing dimensions
14. **Clickable Badges** - Click any badge to learn more

### UI Features:
15. **Dark/Light Mode** - Toggle theme
16. **Responsive Design** - Works on different screen sizes

---

## 🎮 HOW TO DEMONSTRATE TO YOUR PROFESSOR

### Demo Script:

**Step 1: Show the Dashboard**
- Point out the 4 metric cards (Total Records, Total Sales, Units Sold, Avg Sale)
- Explain this is the summary of the sales data

**Step 2: Explain OLAP Concepts**
- Click "OLAP Guide" button → Show the 5 operations
- Click "Data Cube" button → Show the 3D visualization
- Explain: "This cube has 3 dimensions: Time, Region, and Product. The center contains our measures (sales data)."

**Step 3: Demonstrate Natural Language Query**
- Type: "Break down Q4 sales by region"
- Click Send
- Explain: "The system understood this is a SLICE operation (filtering to Q4) and grouped by region"

**Step 4: Show Different OLAP Operations**

| Say This | Type This Query |
|----------|-----------------|
| "This is DRILL-DOWN" | "Drill into North region by month" |
| "This is ROLL-UP" | "Show total sales by category" |
| "This is SLICE" | "Show only Q4 sales" |
| "This is DICE" | "Compare North and South in Q4" |

**Step 5: Show Visualizations**
- Click "Chart Type" dropdown → Switch between Bar, Pie, Line, Area
- Click "Table" tab → Show the raw data

**Step 6: Show Export Features**
- Click "Export" → Show CSV, Excel, PDF options
- Download a PDF report to show professional output

**Step 7: Show Comparison Mode**
- Click "Compare" button
- Select Region → North vs South
- Click "Run Comparison"
- Explain: "This allows side-by-side analysis"

**Step 8: Show Query History**
- Click "History" button
- Click on a query to expand it
- Show: Response, Analysis Details, Top Results
- Explain: "All queries are tracked with full results"

**Step 9: Show Interactive Badges**
- Click on "SLICE" badge → Show operation explanation
- Click on "region" badge → Show dimension info
- Click on "+3" under Products → Show all products

---

## 💡 KEY POINTS TO EXPLAIN TO PROFESSOR

1. **Why OLAP?**
   - Traditional databases are for transactions (OLTP)
   - OLAP is for analysis and decision-making
   - OLAP allows multidimensional analysis

2. **Why Natural Language?**
   - Business users don't know SQL
   - Natural language makes data analysis accessible to everyone
   - Faster insights without technical knowledge

3. **The Data Cube Concept**
   - Data is organized in a cube shape
   - Each axis is a dimension (Time, Region, Product)
   - The cube contains measures (Sales, Quantity)
   - Operations "slice" or "dice" the cube

4. **Real-World Application**
   - Retail companies use this for sales analysis
   - Managers can ask questions without IT help
   - Quick insights for business decisions

---

## 🔑 IMPORTANT TERMS TO KNOW

| Term | Definition |
|------|------------|
| **OLAP** | Online Analytical Processing - technology for multidimensional analysis |
| **Dimension** | A category used to organize data (Region, Time, Product) |
| **Measure** | A numeric value to analyze (Sales Amount, Quantity) |
| **Fact** | A single record in the database |
| **Data Cube** | Multidimensional representation of data |
| **Drill-Down** | Navigate from summary to detail |
| **Roll-Up** | Aggregate from detail to summary |
| **Slice** | Filter on one dimension |
| **Dice** | Filter on multiple dimensions |
| **Pivot** | Rotate the data view |

---

## 🌐 HOW TO ACCESS

**URL:** https://bi-chat-tool.preview.emergentagent.com

The application is live and ready to use. No login required.

---

## 📝 EXAMPLE QUERIES TO TRY

1. "Break down Q4 sales by region"
2. "Show top 5 products by revenue"
3. "Compare sales between North and South"
4. "Drill into Q4 by month for Electronics"
5. "What's the total sales by category?"
6. "Show sales trend by quarter"
7. "Which region has the highest sales?"
8. "Break down Laptop sales by region"

---

## ✅ CHECKLIST FOR PRESENTATION

- [ ] Open the application URL
- [ ] Show the dashboard overview
- [ ] Explain OLAP concepts using the Guide
- [ ] Demonstrate 3-4 different queries
- [ ] Show chart type switching
- [ ] Export a PDF report
- [ ] Show the Data Cube visualization
- [ ] Demonstrate the Comparison Mode
- [ ] Show Query History with expandable details
- [ ] Explain how the system understands natural language

---

**Good luck with your presentation! 🎓**
