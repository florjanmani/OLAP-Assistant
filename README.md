# OLAP Assistant

A natural language OLAP (Online Analytical Processing) system that enables business users to analyze sales data through conversational queries.

## 🎯 Project Overview

This application transforms natural language questions into OLAP operations, allowing users to:
- Analyze 10,000+ sales transactions in a star schema
- Perform drill-down, roll-up, slice, dice, and pivot operations
- Visualize data with multiple chart types (Bar, Pie, Line, Area)
- Export results to CSV, Excel, and PDF
- Compare metrics across dimensions
- Track query history with full result details

**Course:** Kurs Special ne Informatike (Special Course in Informatics)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                     React.js + Tailwind CSS                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Query Input │  │   Charts    │  │   Tables    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    ORCHESTRATOR                              ││
│  │              (Query Classification & Routing)                ││
│  └─────────────────────────────────────────────────────────────┘│
│         │              │              │              │           │
│         ▼              ▼              ▼              ▼           │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ Dimension │  │   Cube    │  │    KPI    │  │  Report   │    │
│  │ Navigator │  │ Operations│  │Calculator │  │ Generator │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DUCKDB                                   │
│                 Star Schema (10,000+ Records)                    │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│    │dim_time  │  │dim_region│  │dim_product│ │fact_sales │      │
│    └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
olap-assistant/
├── backend/
│   ├── server.py              # FastAPI main application
│   ├── agents/
│   │   ├── dimension_navigator.py   # Dimension exploration
│   │   ├── cube_operations.py       # OLAP operations
│   │   ├── kpi_calculator.py        # KPI calculations
│   │   └── report_generator.py      # Report generation
│   ├── planner/
│   │   └── orchestrator.py          # Agent coordination
│   ├── database/
│   │   ├── duckdb_manager.py        # DuckDB operations
│   │   └── schema.sql               # Star schema DDL
│   ├── .env                         # Environment variables
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── OLAPDashboard.jsx    # Main dashboard
│   │   └── components/
│   ├── .env
│   └── package.json
├── data/
│   └── olap_warehouse.duckdb        # DuckDB database file
├── docs/
│   ├── ARCHITECTURE.md              # System architecture
│   ├── AGENT_SPECIFICATIONS.md      # Agent details
│   ├── PROMPT_DESIGN.md             # LLM prompt engineering
│   └── USER_GUIDE.md                # End-user documentation
├── CLAUDE.md                        # Dataset & query guidelines
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- No external database required (DuckDB is embedded)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd olap-assistant
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Create .env file in backend/
LLM_API_KEY=<your-llm-api-key>  # For natural language processing
CORS_ORIGINS="*"
```

4. **Frontend Setup**
```bash
cd frontend
yarn install
```

5. **Start the Application**
```bash
# Terminal 1: Backend
cd backend
uvicorn server:app --reload --port 8001

# Terminal 2: Frontend
cd frontend
yarn start
```

6. **Access the Application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8001/docs (Swagger UI)

The database will be automatically initialized with 10,000+ sample transactions on first startup.

## 📊 Dataset

The application uses a **Star Schema** with **10,000+ transactions**.

### Fact Table: `fact_sales`

| Column | Type | Description |
|--------|------|-------------|
| sales_key | INTEGER | Primary key |
| transaction_id | VARCHAR | Unique transaction ID (TXN-000001) |
| time_key | INTEGER | FK to dim_time |
| region_key | INTEGER | FK to dim_region |
| product_key | INTEGER | FK to dim_product |
| sales_amount | DECIMAL | Sale value in dollars |
| quantity | INTEGER | Units sold |
| unit_price | DECIMAL | Price per unit |
| profit_margin | DECIMAL | Profit margin percentage |

### Dimension Tables

| Table | Records | Description |
|-------|---------|-------------|
| dim_time | ~1,100 | Date hierarchy (2022-2024) |
| dim_region | 5 | North, South, East, West, Central |
| dim_product | 8 | Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones |
| dim_category | 3 | Electronics, Computing, Accessories |

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check |
| POST | `/api/chat` | Process natural language query |
| POST | `/api/data/init` | Initialize/regenerate data |
| GET | `/api/data/summary` | Get data summary |
| POST | `/api/olap/query` | Execute direct OLAP query |
| GET | `/api/olap/sales-by-region` | Sales by region |
| GET | `/api/olap/sales-by-product` | Sales by product |
| GET | `/api/olap/sales-by-month` | Sales by month |
| GET | `/api/agents/status` | Agent health status |
| GET | `/api/agents/capabilities` | Agent capabilities |
| GET | `/api/dimensions` | Available dimensions |
| GET | `/api/kpi/summary` | KPI calculations |
| GET | `/api/operations/{op}` | OLAP operation explanation |

## 🎮 Features

### OLAP Operations
- **Drill-Down**: Navigate from summary to detail (Year → Quarter → Month)
- **Roll-Up**: Aggregate from detail to summary (Product → Category)
- **Slice**: Filter on single dimension (only Q4)
- **Dice**: Filter on multiple dimensions (Q4 AND North)
- **Pivot**: Rotate the data view

### Visualizations
- Bar Charts
- Pie Charts
- Line Charts
- Area Charts
- Data Tables

### Export Options
- CSV Download
- Excel (.xlsx) Export
- PDF Report Generation

### Additional Features
- Query History with expandable details
- Query Bookmarking
- Comparison Mode (side-by-side analysis)
- Filter Builder (visual filter creation)
- Dark/Light Mode
- OLAP Guide (educational component)
- 3D Data Cube Visualization

## 📝 Example Queries

```
"Break down Q4 sales by region"
"Show top 5 products by revenue"
"Compare sales between North and South"
"Drill into Q4 by month for Electronics"
"What's the total sales by category?"
"Show year-over-year growth"
"Which region has the highest profit margin?"
```

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Test API endpoints
curl http://localhost:8001/api/data/summary
```

## 📚 Documentation

- [Architecture Document](docs/ARCHITECTURE.md) - System design and data flow
- [Agent Specifications](docs/AGENT_SPECIFICATIONS.md) - Multi-agent architecture details
- [Prompt Design](docs/PROMPT_DESIGN.md) - LLM prompt engineering approach
- [User Guide](docs/USER_GUIDE.md) - End-user documentation
- [CLAUDE.md](CLAUDE.md) - Dataset documentation and query guidelines

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React.js 18 | UI Framework |
| Styling | Tailwind CSS | Utility-first CSS |
| Charts | Recharts | Data visualization |
| UI Components | shadcn/ui | Component library |
| Backend | FastAPI | REST API server |
| Database | DuckDB | OLAP-optimized embedded database |
| Language Model | Claude | Natural language understanding |

## 📄 License

This project is for educational purposes - Kurs Special ne Informatike.

---

## Contributors

Built as a school project demonstrating OLAP concepts, natural language processing, and multi-agent system architecture.
