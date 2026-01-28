# OLAP Assistant

A natural language OLAP (Online Analytical Processing) system that enables business users to analyze sales data through conversational queries.

## 🎯 Project Overview

This application transforms natural language questions into OLAP operations, allowing users to:
- Analyze 10,000+ sales transactions
- Perform drill-down, roll-up, slice, dice, and pivot operations
- Visualize data with multiple chart types
- Export results to CSV, Excel, and PDF
- Compare metrics across dimensions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                     React.js + Tailwind                          │
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
│                        MONGODB                                   │
│                    (10,000+ Records)                             │
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
│   │   └── schema.sql               # Star schema DDL
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── OLAPDashboard.jsx    # Main dashboard
│   │   └── components/
│   └── package.json
├── data/
│   └── sales.csv                    # Sample dataset
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENT_SPECIFICATIONS.md
│   ├── PROMPT_DESIGN.md
│   └── USER_GUIDE.md
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB

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
MONGO_URL="mongodb://localhost:27017"
DB_NAME="olap_database"
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
- API Docs: http://localhost:8001/docs

## 📊 Dataset

The application includes a generated dataset with **10,000+ transactions**:

| Field | Description | Values |
|-------|-------------|--------|
| region | Geographic area | North, South, East, West, Central |
| product | Item sold | Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones |
| category | Product group | Electronics, Computing, Accessories |
| sales_amount | Sale value | $500 - $50,000 |
| quantity | Units sold | 1 - 50 |
| quarter | Fiscal quarter | Q1, Q2, Q3, Q4 |
| year | Year | 2022, 2023, 2024 |

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check |
| POST | `/api/chat` | Process natural language query |
| POST | `/api/data/init` | Initialize sample data |
| GET | `/api/data/summary` | Get data summary |
| POST | `/api/olap/query` | Execute OLAP query |
| GET | `/api/olap/sales-by-region` | Sales by region |
| GET | `/api/olap/sales-by-product` | Sales by product |

## 🎮 Features

### OLAP Operations
- **Drill-Down**: Navigate from summary to detail
- **Roll-Up**: Aggregate from detail to summary
- **Slice**: Filter on single dimension
- **Dice**: Filter on multiple dimensions
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
- Comparison Mode
- Filter Builder
- Dark/Light Mode

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

# Run frontend tests
cd frontend
yarn test
```

## 📚 Documentation

- [Architecture Document](docs/ARCHITECTURE.md)
- [Agent Specifications](docs/AGENT_SPECIFICATIONS.md)
- [Prompt Design](docs/PROMPT_DESIGN.md)
- [User Guide](docs/USER_GUIDE.md)

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React.js, Tailwind CSS, Recharts |
| Backend | FastAPI, Python |
| Database | MongoDB |
| Charts | Recharts |

## 📄 License

This project is for educational purposes - Kurs Special ne Informatike.
