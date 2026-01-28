# API Documentation

## Overview

The OLAP Assistant API provides RESTful endpoints for natural language OLAP analysis.

**Base URL:** `http://localhost:8001` (Development) or your deployed URL

**API Prefix:** All endpoints are prefixed with `/api/`

**Swagger UI:** Available at `http://localhost:8001/docs`

---

## Authentication

No authentication required for this educational project.

---

## Endpoints

### Health Check

**GET** `/api/`

Returns API status.

**Response:**
```json
{
  "message": "OLAP Assistant API"
}
```

---

### Natural Language Chat

**POST** `/api/chat`

Process a natural language query and return OLAP analysis results.

**Request Body:**
```json
{
  "message": "Show Q4 sales by region",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Filtering sales data to Q4 and grouping by region...",
  "analysis_result": {
    "operation": "slice",
    "dimensions": ["region"],
    "measures": ["sales_amount"],
    "filters": {"quarter": "Q4"},
    "data": [
      {"region": "North", "total_sales_amount": 12500000, "count": 580}
    ],
    "row_count": 5
  },
  "session_id": "uuid-session-id"
}
```

---

### Chat History

**GET** `/api/chat/history/{session_id}`

Retrieve chat history for a session.

**Parameters:**
- `session_id` (path): Session identifier

**Response:**
```json
{
  "messages": [
    {
      "id": "msg-id",
      "role": "user",
      "content": "Show sales by region",
      "timestamp": "2024-01-28T10:30:00Z"
    }
  ]
}
```

---

### Data Summary

**GET** `/api/data/summary`

Get summary statistics of the data warehouse.

**Response:**
```json
{
  "total_records": 11000,
  "total_sales": 224554317.44,
  "total_quantity": 279707,
  "avg_sale": 20414.03,
  "dimensions": {
    "regions": ["Central", "East", "North", "South", "West"],
    "products": ["Desktop", "Headphones", "Keyboard", "Laptop", "Monitor", "Mouse", "Phone", "Tablet"],
    "quarters": ["Q1", "Q2", "Q3", "Q4"],
    "years": [2022, 2023, 2024]
  }
}
```

---

### Initialize Data

**POST** `/api/data/init`

Initialize or regenerate the sample data.

**Response:**
```json
{
  "message": "Data initialized with star schema",
  "record_count": 11000
}
```

---

### Direct OLAP Query

**POST** `/api/olap/query`

Execute a direct OLAP query with specific parameters.

**Request Body:**
```json
{
  "operation": "slice",
  "dimensions": ["region"],
  "measures": ["sales_amount", "quantity"],
  "filters": {"quarter": "Q4"}
}
```

**Response:**
```json
{
  "operation": "slice",
  "dimensions": ["region"],
  "measures": ["sales_amount", "quantity"],
  "filters": {"quarter": "Q4"},
  "data": [...],
  "row_count": 5
}
```

---

### Sales by Region

**GET** `/api/olap/sales-by-region`

Get sales breakdown by region.

**Query Parameters:**
- `quarter` (optional): Filter by quarter (Q1, Q2, Q3, Q4)
- `year` (optional): Filter by year (2022, 2023, 2024)

**Example:** `/api/olap/sales-by-region?quarter=Q4&year=2024`

**Response:**
```json
{
  "operation": "aggregate",
  "dimensions": ["region"],
  "data": [
    {
      "region": "North",
      "total_sales_amount": 47817761.80,
      "avg_sales_amount": 21167.67,
      "total_quantity": 57506,
      "count": 2259
    }
  ],
  "row_count": 5
}
```

---

### Sales by Product

**GET** `/api/olap/sales-by-product`

Get sales breakdown by product.

**Query Parameters:**
- `region` (optional): Filter by region
- `quarter` (optional): Filter by quarter

---

### Sales by Month

**GET** `/api/olap/sales-by-month`

Get sales breakdown by month.

**Query Parameters:**
- `year` (optional): Filter by year
- `region` (optional): Filter by region

---

### Agent Status

**GET** `/api/agents/status`

Get status of all agents.

**Response:**
```json
{
  "dimension_navigator": "active",
  "cube_operations": "active",
  "kpi_calculator": "active",
  "report_generator": "active"
}
```

---

### Agent Capabilities

**GET** `/api/agents/capabilities`

Get capabilities of all agents.

**Response:**
```json
{
  "dimension_navigator": [
    "List available dimensions",
    "Show dimension hierarchies",
    "Get dimension values",
    "Suggest drill paths"
  ],
  "cube_operations": [
    "Drill-down analysis",
    "Roll-up aggregation",
    "Slice (single filter)",
    "Dice (multiple filters)",
    "Pivot operations"
  ],
  "kpi_calculator": [...],
  "report_generator": [...]
}
```

---

### Dimensions

**GET** `/api/dimensions`

Get all available dimensions.

**Response:**
```json
{
  "dimensions": [
    {
      "name": "Time",
      "type": "time",
      "hierarchy": ["Year", "Quarter", "Month", "Day"],
      "values_count": 3
    }
  ]
}
```

---

### Dimension Details

**GET** `/api/dimensions/{dimension_name}`

Get details for a specific dimension.

**Parameters:**
- `dimension_name` (path): time, geography, or product

**Response:**
```json
{
  "dimension": "time",
  "hierarchy": ["Year", "Quarter", "Month", "Day"],
  "values": ["2022", "2023", "2024"]
}
```

---

### KPI Summary

**GET** `/api/kpi/summary`

Get KPI summary metrics.

**Response:**
```json
{
  "total_revenue": 224554317.44,
  "total_revenue_formatted": "$224,554,317.44",
  "total_units_sold": 279707,
  "num_transactions": 11000,
  "average_order_value": 20414.03,
  "average_profit_margin": 30.12,
  "revenue_per_unit": 802.81
}
```

---

### Operation Explanation

**GET** `/api/operations/{operation}`

Get explanation for an OLAP operation.

**Parameters:**
- `operation` (path): drill_down, roll_up, slice, dice, pivot

**Response:**
```json
{
  "name": "Drill-Down",
  "description": "Navigate from summary to detailed data by moving down the hierarchy.",
  "example": "Year → Quarter → Month → Day",
  "use_case": "When you want to see more granular details"
}
```

---

### Export Sample Data

**GET** `/api/export/sample-data`

Export sample sales data.

**Query Parameters:**
- `limit` (optional): Number of records (default: 100)

**Response:**
```json
{
  "columns": ["transaction_id", "date", "quarter", ...],
  "data": [...],
  "count": 100
}
```

---

## Error Responses

All endpoints return standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

**Error Format:**
```json
{
  "detail": "Error description"
}
```

---

## Data Types

### ChatRequest
```typescript
{
  message: string;       // Required: Natural language query
  session_id?: string;   // Optional: Session identifier
}
```

### OLAPQuery
```typescript
{
  operation: string;     // Required: OLAP operation type
  dimensions: string[];  // Required: Dimensions to group by
  measures: string[];    // Required: Measures to calculate
  filters?: object;      // Optional: Filter conditions
}
```

### AnalysisResult
```typescript
{
  operation: string;
  dimensions: string[];
  measures: string[];
  filters: object;
  data: object[];
  row_count: number;
}
```
