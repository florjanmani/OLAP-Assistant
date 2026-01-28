"""
OLAP Assistant - FastAPI Backend Server
Integrates with DuckDB Star Schema and Multi-Agent Architecture
"""

from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import json

# Import database manager
from database.duckdb_manager import db_manager

# Import agents
from agents.dimension_navigator import dimension_navigator
from agents.cube_operations import cube_operations
from agents.kpi_calculator import kpi_calculator
from agents.report_generator import report_generator
from planner.orchestrator import orchestrator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app with API docs under /api prefix
app = FastAPI(
    title="OLAP Assistant API",
    description="Natural Language OLAP Analysis System with Multi-Agent Architecture",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory chat history store (for simplicity, could use DB)
chat_sessions: Dict[str, List[Dict]] = {}


# Define Models
class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    analysis_result: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    analysis_result: Optional[Dict[str, Any]] = None
    session_id: str


class OLAPQuery(BaseModel):
    operation: str  # drill_down, roll_up, slice, dice, pivot
    dimensions: List[str]
    measures: List[str]
    filters: Optional[Dict[str, Any]] = None


class CompareRequest(BaseModel):
    dimension: str  # region, product, quarter, etc.
    item1: str
    item2: str


# OLAP System Prompt
OLAP_SYSTEM_PROMPT = """You are an OLAP (Online Analytical Processing) Assistant that helps business users analyze sales data through natural language.

Available Data Schema (Star Schema):
- Dimensions: region, product, category, quarter, month, year
- Measures: sales_amount, quantity, profit_margin
- Regions: North, South, East, West, Central
- Products: Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones  
- Categories: Electronics, Accessories, Computing
- Time: Years 2022-2024, Quarters Q1-Q4, Months January-December

OLAP Operations You Can Perform:
1. DRILL-DOWN: Go from summary to detail (e.g., Year → Quarter → Month)
2. ROLL-UP: Aggregate from detail to summary (e.g., Product → Category)
3. SLICE: Filter data on one dimension (e.g., only Q4)
4. DICE: Filter on multiple dimensions (e.g., Q4 AND North region)
5. PIVOT: Rotate dimensions for different views

When a user asks a question, analyze it and return a JSON object with:
{
    "operation": "drill_down|roll_up|slice|dice|pivot|aggregate",
    "dimensions": ["list of dimensions to group by"],
    "measures": ["sales_amount", "quantity"],
    "filters": {"dimension": "value or [values]"},
    "explanation": "Brief explanation of what analysis you're performing"
}

Examples:
- "Show Q4 sales by region" → {"operation": "slice", "dimensions": ["region"], "measures": ["sales_amount"], "filters": {"quarter": "Q4"}, "explanation": "Filtering sales data to Q4 and grouping by region"}
- "Drill into North region by month" → {"operation": "drill_down", "dimensions": ["month"], "measures": ["sales_amount"], "filters": {"region": "North"}, "explanation": "Drilling down into North region sales by month"}
- "What's the total sales by category?" → {"operation": "aggregate", "dimensions": ["category"], "measures": ["sales_amount"], "filters": {}, "explanation": "Aggregating total sales by product category"}

Always respond with valid JSON followed by a friendly explanation for business users."""


async def process_natural_language_query(message: str, session_id: str) -> Dict[str, Any]:
    """Process natural language query using LLM and execute OLAP analysis."""
    # Support multiple env var names for flexibility
    api_key = os.environ.get('LLM_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        raise HTTPException(status_code=500, detail="LLM API key not configured. Set LLM_API_KEY or ANTHROPIC_API_KEY in .env")
    
    # Use the LLM chat library
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id,
        system_message=OLAP_SYSTEM_PROMPT
    ).with_model("anthropic", "claude-sonnet-4-5-20250929")
    
    user_message = UserMessage(text=message)
    
    try:
        response = await chat.send_message(user_message)
        
        # Parse JSON from response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end]
            query_params = json.loads(json_str)
            
            # Execute the OLAP analysis using DuckDB
            analysis_result = db_manager.execute_olap_query(
                dimensions=query_params.get("dimensions", ["region"]),
                measures=query_params.get("measures", ["sales_amount"]),
                filters=query_params.get("filters", {}),
                operation=query_params.get("operation", "aggregate")
            )
            
            # Get the explanation
            explanation = query_params.get("explanation", "")
            remaining_text = response[json_end:].strip() if json_end < len(response) else ""
            
            return {
                "response": f"{explanation}\n\n{remaining_text}".strip(),
                "analysis_result": analysis_result,
                "query_params": query_params
            }
        else:
            return {
                "response": response,
                "analysis_result": None,
                "query_params": None
            }
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return {
            "response": response if 'response' in dir() else "I had trouble understanding that query. Could you rephrase it?",
            "analysis_result": None,
            "query_params": None
        }
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API Routes
@api_router.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "OLAP Assistant API"}


@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Process natural language OLAP query."""
    session_id = request.session_id or str(uuid.uuid4())
    
    result = await process_natural_language_query(request.message, session_id)
    
    # Store message in session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    user_msg = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    chat_sessions[session_id].append(user_msg)
    
    assistant_msg = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "assistant",
        "content": result["response"],
        "analysis_result": result["analysis_result"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    chat_sessions[session_id].append(assistant_msg)
    
    return ChatResponse(
        response=result["response"],
        analysis_result=result["analysis_result"],
        session_id=session_id
    )


@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session."""
    messages = chat_sessions.get(session_id, [])
    return {"messages": messages}


@api_router.post("/data/init")
async def initialize_data():
    """Initialize the DuckDB star schema with sample data."""
    count = db_manager.initialize_all()
    return {"message": "Data initialized with star schema", "record_count": count}


@api_router.get("/data/summary")
async def get_data_summary():
    """Get summary statistics of the sales data."""
    return db_manager.get_summary()


@api_router.post("/olap/query")
async def execute_olap_query(query: OLAPQuery):
    """Execute a direct OLAP query on the star schema."""
    result = db_manager.execute_olap_query(
        dimensions=query.dimensions,
        measures=query.measures,
        filters=query.filters or {},
        operation=query.operation
    )
    return result


@api_router.get("/olap/sales-by-region")
async def sales_by_region(quarter: Optional[str] = None, year: Optional[int] = None):
    """Get sales breakdown by region."""
    filters = {}
    if quarter:
        filters["quarter"] = quarter
    if year:
        filters["year"] = year
    
    return db_manager.execute_olap_query(
        dimensions=["region"],
        measures=["sales_amount", "quantity"],
        filters=filters,
        operation="aggregate"
    )


@api_router.get("/olap/sales-by-product")
async def sales_by_product(region: Optional[str] = None, quarter: Optional[str] = None):
    """Get sales breakdown by product."""
    filters = {}
    if region:
        filters["region"] = region
    if quarter:
        filters["quarter"] = quarter
    
    return db_manager.execute_olap_query(
        dimensions=["product"],
        measures=["sales_amount", "quantity"],
        filters=filters,
        operation="aggregate"
    )


@api_router.get("/olap/sales-by-month")
async def sales_by_month(year: Optional[int] = None, region: Optional[str] = None):
    """Get sales breakdown by month."""
    filters = {}
    if year:
        filters["year"] = year
    if region:
        filters["region"] = region
    
    return db_manager.execute_olap_query(
        dimensions=["month", "quarter"],
        measures=["sales_amount", "quantity"],
        filters=filters,
        operation="aggregate"
    )


@api_router.post("/compare")
async def compare_items(request: CompareRequest):
    """Compare two items within a dimension."""
    dimension = request.dimension.lower()
    item1 = request.item1
    item2 = request.item2
    
    # Map dimension to filter key
    dim_filter_map = {
        "region": "region",
        "product": "product",
        "category": "category",
        "quarter": "quarter",
        "month": "month",
        "year": "year"
    }
    
    if dimension not in dim_filter_map:
        raise HTTPException(status_code=400, detail=f"Invalid dimension: {dimension}")
    
    filter_key = dim_filter_map[dimension]
    
    # Get data for item1
    result1 = db_manager.execute_olap_query(
        dimensions=[dimension],
        measures=["sales_amount", "quantity"],
        filters={filter_key: item1},
        operation="aggregate"
    )
    
    # Get data for item2
    result2 = db_manager.execute_olap_query(
        dimensions=[dimension],
        measures=["sales_amount", "quantity"],
        filters={filter_key: item2},
        operation="aggregate"
    )
    
    # Calculate comparison metrics
    data1 = result1.get("data", [{}])[0] if result1.get("data") else {}
    data2 = result2.get("data", [{}])[0] if result2.get("data") else {}
    
    sales1 = float(data1.get("total_sales_amount", 0) or 0)
    sales2 = float(data2.get("total_sales_amount", 0) or 0)
    qty1 = int(data1.get("total_quantity", 0) or 0)
    qty2 = int(data2.get("total_quantity", 0) or 0)
    count1 = int(data1.get("count", 0) or 0)
    count2 = int(data2.get("count", 0) or 0)
    
    # Calculate differences
    sales_diff = sales1 - sales2
    sales_diff_pct = ((sales1 - sales2) / sales2 * 100) if sales2 > 0 else 0
    
    return {
        "dimension": dimension,
        "comparison": {
            "item1": {
                "name": item1,
                "total_sales": round(sales1, 2),
                "total_quantity": qty1,
                "transaction_count": count1,
                "avg_sale": round(sales1 / count1, 2) if count1 > 0 else 0
            },
            "item2": {
                "name": item2,
                "total_sales": round(sales2, 2),
                "total_quantity": qty2,
                "transaction_count": count2,
                "avg_sale": round(sales2 / count2, 2) if count2 > 0 else 0
            },
            "difference": {
                "sales_amount": round(sales_diff, 2),
                "sales_percentage": round(sales_diff_pct, 2),
                "winner": item1 if sales1 > sales2 else item2
            }
        },
        "chart_data": [
            {"name": item1, "sales": round(sales1, 2), "quantity": qty1},
            {"name": item2, "sales": round(sales2, 2), "quantity": qty2}
        ]
    }


# Agent-specific endpoints
@api_router.get("/agents/status")
async def get_agent_status():
    """Get status of all agents."""
    return orchestrator.get_agent_status()


@api_router.get("/agents/capabilities")
async def get_agent_capabilities():
    """Get capabilities of all agents."""
    return orchestrator.get_capabilities()


@api_router.get("/dimensions")
async def get_dimensions():
    """Get all available dimensions from the Dimension Navigator agent."""
    return {"dimensions": dimension_navigator.get_all_dimensions()}


@api_router.get("/dimensions/{dimension_name}")
async def get_dimension_details(dimension_name: str):
    """Get details for a specific dimension."""
    hierarchy = dimension_navigator.get_dimension_hierarchy(dimension_name)
    values = dimension_navigator.get_dimension_values(dimension_name)
    
    if hierarchy is None:
        raise HTTPException(status_code=404, detail=f"Dimension '{dimension_name}' not found")
    
    return {
        "dimension": dimension_name,
        "hierarchy": hierarchy,
        "values": values
    }


@api_router.get("/kpi/summary")
async def get_kpi_summary():
    """Get KPI summary using the KPI Calculator agent."""
    # Get raw data from DuckDB
    result = db_manager.conn.execute("""
        SELECT 
            f.sales_amount, 
            f.quantity, 
            f.profit_margin,
            t.year, 
            t.quarter
        FROM fact_sales f
        JOIN dim_time t ON f.time_key = t.time_key
    """).fetchall()
    
    # Convert to list of dicts for KPI calculator
    data = [
        {
            "sales_amount": row[0],
            "quantity": row[1],
            "profit_margin": row[2],
            "year": row[3],
            "quarter": row[4]
        }
        for row in result
    ]
    
    return kpi_calculator.get_kpi_summary(data)


@api_router.get("/operations/{operation}")
async def get_operation_explanation(operation: str):
    """Get explanation for an OLAP operation from Cube Operations agent."""
    return cube_operations.get_operation_explanation(operation)


@api_router.get("/export/sample-data")
async def export_sample_data(limit: int = 100):
    """Export sample sales data as JSON (for CSV conversion on frontend)."""
    result = db_manager.conn.execute(f"""
        SELECT 
            f.transaction_id,
            t.full_date,
            t.quarter,
            t.month_name,
            t.year,
            r.region_name as region,
            p.product_name as product,
            p.category_name as category,
            f.sales_amount,
            f.quantity,
            f.unit_price,
            f.profit_margin
        FROM fact_sales f
        JOIN dim_time t ON f.time_key = t.time_key
        JOIN dim_region r ON f.region_key = r.region_key
        JOIN dim_product p ON f.product_key = p.product_key
        ORDER BY f.sales_key
        LIMIT {limit}
    """).fetchall()
    
    columns = ['transaction_id', 'date', 'quarter', 'month', 'year', 
               'region', 'product', 'category', 'sales_amount', 
               'quantity', 'unit_price', 'profit_margin']
    
    data = []
    for row in result:
        record = {}
        for i, col in enumerate(columns):
            val = row[i]
            if hasattr(val, 'isoformat'):
                val = val.isoformat()
            elif isinstance(val, float):
                val = round(val, 2)
            record[col] = val
        data.append(record)
    
    return {"columns": columns, "data": data, "count": len(data)}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and sample data on startup."""
    logger.info("Starting OLAP Assistant...")
    count = db_manager.initialize_all()
    logger.info(f"Database initialized with {count} records")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    db_manager.close()
