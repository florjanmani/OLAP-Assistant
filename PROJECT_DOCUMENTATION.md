# OLAP Assistant - Complete Project Documentation
## Kurs Special ne Informatike - School Project

---

## 📋 WHAT IS THIS PROJECT?

This is an **OLAP Assistant** - a web application that allows business users to analyze sales data using **natural language** instead of writing SQL queries. 

**Example:** Instead of writing complex SQL like:
```sql
SELECT r.region_name, SUM(f.sales_amount) 
FROM fact_sales f
JOIN dim_time t ON f.time_key = t.time_key
JOIN dim_region r ON f.region_key = r.region_key
WHERE t.quarter = 'Q4' 
GROUP BY r.region_name
ORDER BY SUM(f.sales_amount) DESC
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
- **Facts** = The actual transaction records

### The 5 OLAP Operations:

| Operation | What it Does | Example |
|-----------|--------------|---------|
| **Drill-Down** | Go from summary → detail | Year → Quarter → Month |
| **Roll-Up** | Go from detail → summary | Product → Category |
| **Slice** | Filter on ONE dimension | Only show Q4 data |
| **Dice** | Filter on MULTIPLE dimensions | Q4 AND North region |
| **Pivot** | Rotate the view | Swap rows and columns |

---

## 🏗️ ARCHITECTURE OVERVIEW

The system uses a **multi-agent architecture** with a **star schema database**:

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                           │
│                   React.js + Tailwind CSS                        │
│         (Charts, Tables, Query Input, Export Options)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API LAYER (FastAPI)                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      ORCHESTRATOR                           │ │
│  │        (Query Classification & Agent Routing)               │ │
│  └────────────────────────────────────────────────────────────┘ │
│       │              │              │              │             │
│       ▼              ▼              ▼              ▼             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐         │
│  │Dimension│   │  Cube   │   │   KPI   │   │ Report  │         │
│  │Navigator│   │Operations│   │Calculator│   │Generator│         │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (DuckDB)                         │
│                                                                  │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│     │dim_time  │  │dim_region│  │dim_product│  (Dimensions)     │
│     └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│          │             │             │                          │
│          └─────────────┼─────────────┘                          │
│                        │                                         │
│                 ┌──────┴──────┐                                  │
│                 │ fact_sales  │  (10,000+ transactions)         │
│                 └─────────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Purpose |
|-------|---------|
| **Dimension Navigator** | Explore dimensions, show hierarchies, suggest drill paths |
| **Cube Operations** | Execute OLAP operations (drill-down, roll-up, slice, dice, pivot) |
| **KPI Calculator** | Calculate growth rates, margins, averages |
| **Report Generator** | Format reports, generate summaries |
| **Orchestrator** | Classify query intent, route to appropriate agent |

---

## 📊 THE DATASET

The application uses a **Star Schema** database with **10,000+ transactions**.

### Star Schema Design

```
                          dim_time
                        ┌───────────┐
                        │ time_key  │
                        │ full_date │
                        │ quarter   │
                        │ month     │
                        │ year      │
                        └─────┬─────┘
                              │
   dim_region                 │                dim_product
  ┌───────────┐               │              ┌─────────────┐
  │region_key │               │              │ product_key │
  │region_name│               │              │ product_name│
  │ (5 rows)  │               │              │ category    │
  └─────┬─────┘               │              └──────┬──────┘
        │                     │                     │
        └──────────┬──────────┴──────────┬─────────┘
                   │                     │
              ┌────┴─────────────────────┴────┐
              │         fact_sales            │
              │  ┌─────────────────────────┐  │
              │  │ sales_key (PK)          │  │
              │  │ transaction_id          │  │
              │  │ time_key (FK)           │  │
              │  │ region_key (FK)         │  │
              │  │ product_key (FK)        │  │
              │  │ sales_amount            │  │
              │  │ quantity                │  │
              │  │ profit_margin           │  │
              │  │ (10,000+ rows)          │  │
              │  └─────────────────────────┘  │
              └───────────────────────────────┘
```

### Data Summary

| Metric | Value |
|--------|-------|
| **Total Records** | 10,000+ transactions |
| **Total Sales** | ~$224 million |
| **Total Units Sold** | ~280,000 |
| **Average Transaction** | ~$20,400 |
| **Date Range** | 2022 - 2024 |

### Dimension Values

| Dimension | Values |
|-----------|--------|
| **Regions** | North, South, East, West, Central |
| **Products** | Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones |
| **Categories** | Electronics, Computing, Accessories |
| **Quarters** | Q1, Q2, Q3, Q4 |
| **Years** | 2022, 2023, 2024 |

---

## 🛠️ TECHNOLOGY STACK

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React.js 18 | User interface |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Charts** | Recharts | Data visualizations (Bar, Pie, Line, Area) |
| **UI Components** | shadcn/ui | Pre-built UI components |
| **Backend** | FastAPI (Python) | REST API server |
| **Database** | DuckDB | OLAP-optimized embedded database |
| **LLM Integration** | Claude Sonnet | Natural language understanding |

---

## ✨ FEATURES IMPLEMENTED

### Core OLAP Features
1. ✅ **Natural Language Queries** - Ask questions in plain English
2. ✅ **Query Processing** - System understands and executes OLAP operations
3. ✅ **All 5 OLAP Operations** - Drill-down, Roll-up, Slice, Dice, Pivot
4. ✅ **Star Schema Database** - Proper dimensional modeling

### Visualization Features
5. ✅ **Bar Charts** - Compare values across categories
6. ✅ **Pie Charts** - Show proportions
7. ✅ **Line Charts** - View trends
8. ✅ **Area Charts** - Cumulative views
9. ✅ **Data Tables** - Raw data display

### Export & Persistence
10. ✅ **CSV Export** - Download data as spreadsheet
11. ✅ **Excel Export** - Download as .xlsx file
12. ✅ **PDF Report** - Professional formatted report
13. ✅ **Query Bookmarking** - Save favorite queries
14. ✅ **Query History** - View all past queries with results

### Interactive Features
15. ✅ **Filter Builder** - Visual filter creation
16. ✅ **Comparison Mode** - Side-by-side analysis
17. ✅ **Clickable Badges** - Learn about operations
18. ✅ **Dark/Light Mode** - Theme toggle

### Educational Features
19. ✅ **OLAP Guide** - Explains all 5 operations with examples
20. ✅ **Data Cube Visualization** - 3D diagram of data structure

---

## 🎮 HOW TO DEMONSTRATE TO YOUR PROFESSOR

### Demo Script

**Step 1: Show the Dashboard**
- Point out the 4 metric cards (Total Records, Total Sales, Units Sold, Avg Sale)
- Note: "This shows 10,000+ transactions worth over $224 million"

**Step 2: Explain Architecture**
- Click "OLAP Guide" → Show the 5 operations
- Click "Data Cube" → Show the 3D visualization
- Explain: "This system uses a star schema with fact and dimension tables"

**Step 3: Demonstrate Multi-Agent System**
- Open Swagger API docs at `/docs`
- Show `/api/agents/status` endpoint
- Show `/api/agents/capabilities` endpoint
- Explain: "Four specialized agents handle different query types"

**Step 4: Natural Language Queries**
- Type: "Break down Q4 sales by region" (SLICE)
- Type: "Drill into North by month" (DRILL-DOWN)
- Type: "Show total by category" (ROLL-UP)
- Type: "Compare North and South in Q4" (DICE)

**Step 5: Show Visualizations**
- Click chart type dropdown → Switch between Bar, Pie, Line, Area
- Click "Table" tab → Show raw data

**Step 6: Show Export Features**
- Click "Export" → Download PDF report
- Show the generated PDF

**Step 7: Show Comparison Mode**
- Click "Compare" → Select Region → North vs South
- Click "Run Comparison" → Show side-by-side results

**Step 8: Show Query History**
- Click "History" → Expand a query → Show full results stored

---

## 💡 KEY CONCEPTS FOR PRESENTATION

### Why Star Schema?
- **Fact Table**: Contains transaction measures (sales, quantity)
- **Dimension Tables**: Contain descriptive attributes (region names, product names, dates)
- **Benefits**: Optimized for aggregation queries, clear relationships, easy to understand

### Why Multi-Agent Architecture?
- **Separation of Concerns**: Each agent specializes in one task
- **Extensibility**: New agents can be added without changing others
- **Maintainability**: Easier to test and debug individual agents

### Why DuckDB?
- **OLAP Optimized**: Designed for analytical queries
- **Embedded**: No external server needed
- **Fast**: Columnar storage for quick aggregations

---

## 📝 EXAMPLE QUERIES TO TRY

| Query | OLAP Operation |
|-------|----------------|
| "Break down Q4 sales by region" | SLICE |
| "Drill into North region by month" | DRILL-DOWN |
| "Show total sales by category" | ROLL-UP |
| "Compare North and South in Q4" | DICE |
| "Show products by region" | AGGREGATE |
| "What's the year-over-year growth?" | KPI |

---

## 📁 PROJECT DELIVERABLES

| Deliverable | Location | Status |
|-------------|----------|--------|
| Source Code | GitHub Repository | ✅ Complete |
| Working Demo | Live URL | ✅ Complete |
| Database Schema | `/backend/database/schema.sql` | ✅ Complete |
| API Documentation | `/docs` endpoint (Swagger) | ✅ Complete |
| Architecture Document | `/docs/ARCHITECTURE.md` | ✅ Complete |
| Agent Specifications | `/docs/AGENT_SPECIFICATIONS.md` | ✅ Complete |
| Prompt Design | `/docs/PROMPT_DESIGN.md` | ✅ Complete |
| User Guide | `/docs/USER_GUIDE.md` | ✅ Complete |
| README | `/README.md` | ✅ Complete |
| CLAUDE.md | `/CLAUDE.md` | ✅ Complete |
| Demo Video | (To be recorded by user) | ⏳ Pending |

---

## ✅ CHECKLIST FOR PRESENTATION

- [ ] Open the application URL
- [ ] Show 10,000+ records in dashboard
- [ ] Explain star schema using Data Cube visualization
- [ ] Explain multi-agent architecture using API docs
- [ ] Demonstrate 3-4 different OLAP operations
- [ ] Show chart type switching
- [ ] Export a PDF report
- [ ] Show Comparison Mode
- [ ] Show Query History with expandable details
- [ ] Explain how natural language becomes SQL

---

**Good luck with your presentation! 🎓**
