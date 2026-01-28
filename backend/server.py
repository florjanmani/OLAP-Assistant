from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import random
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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

class SalesData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    region: str
    product: str
    category: str
    sales_amount: float
    quantity: int
    date: str
    quarter: str
    month: str
    year: int

class OLAPQuery(BaseModel):
    operation: str  # drill_down, roll_up, slice, dice, pivot
    dimensions: List[str]
    measures: List[str]
    filters: Optional[Dict[str, Any]] = None

# Sample data configuration
REGIONS = ["North", "South", "East", "West", "Central"]
PRODUCTS = ["Laptop", "Desktop", "Tablet", "Phone", "Monitor", "Keyboard", "Mouse", "Headphones"]
CATEGORIES = ["Electronics", "Accessories", "Computing"]
MONTHS = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]

PRODUCT_CATEGORY_MAP = {
    "Laptop": "Computing", "Desktop": "Computing", "Tablet": "Computing",
    "Phone": "Electronics", "Monitor": "Electronics",
    "Keyboard": "Accessories", "Mouse": "Accessories", "Headphones": "Accessories"
}

# Helper functions
def get_quarter(month_idx: int) -> str:
    if month_idx < 3:
        return "Q1"
    elif month_idx < 6:
        return "Q2"
    elif month_idx < 9:
        return "Q3"
    else:
        return "Q4"

async def generate_sample_data():
    """Generate sample sales data for OLAP analysis - 10,000+ transactions"""
    existing = await db.sales_data.count_documents({})
    if existing >= 10000:
        logger.info(f"Sample data already exists: {existing} records")
        return existing
    
    # Clear existing data to regenerate with 10,000+ records
    if existing > 0 and existing < 10000:
        await db.sales_data.delete_many({})
        logger.info("Cleared existing data to regenerate 10,000+ records")
    
    sales_data = []
    transaction_id = 1
    
    # Generate data for 3 years to reach 10,000+ transactions
    for year in [2022, 2023, 2024]:
        for month_idx, month in enumerate(MONTHS):
            quarter = get_quarter(month_idx)
            for region in REGIONS:
                for product in PRODUCTS:
                    # Generate multiple transactions per product/region/month
                    num_transactions = random.randint(2, 5)  # 2-5 transactions each
                    
                    for _ in range(num_transactions):
                        # Generate realistic sales with variation
                        base_sales = random.uniform(500, 15000)
                        
                        # Q4 generally has higher sales (holiday season)
                        if quarter == "Q4":
                            base_sales *= 1.3
                        
                        # Some regions perform better
                        if region in ["North", "East"]:
                            base_sales *= 1.15
                        elif region == "Central":
                            base_sales *= 1.05
                        
                        # Product-based pricing
                        if product in ["Laptop", "Desktop"]:
                            base_sales *= 2.5
                        elif product in ["Phone", "Tablet"]:
                            base_sales *= 1.8
                        elif product == "Monitor":
                            base_sales *= 1.4
                        
                        # Random day in month
                        day = random.randint(1, 28)
                        quantity = random.randint(1, 50)
                        
                        sales_data.append({
                            "id": str(uuid.uuid4()),
                            "transaction_id": f"TXN-{transaction_id:06d}",
                            "region": region,
                            "product": product,
                            "category": PRODUCT_CATEGORY_MAP[product],
                            "sales_amount": round(base_sales, 2),
                            "quantity": quantity,
                            "unit_price": round(base_sales / quantity, 2),
                            "date": f"{year}-{str(month_idx + 1).zfill(2)}-{str(day).zfill(2)}",
                            "quarter": quarter,
                            "month": month,
                            "year": year,
                            "profit_margin": round(random.uniform(0.15, 0.45), 2),
                            "discount": round(random.uniform(0, 0.20), 2)
                        })
                        transaction_id += 1
    
    await db.sales_data.insert_many(sales_data)
    logger.info(f"Generated {len(sales_data)} sample sales records")
    return len(sales_data)
                    quantity = random.randint(10, 200)
                    
                    sales_data.append({
                        "id": str(uuid.uuid4()),
                        "region": region,
                        "product": product,
                        "category": PRODUCT_CATEGORY_MAP[product],
                        "sales_amount": round(base_sales, 2),
                        "quantity": quantity,
                        "date": f"{year}-{str(month_idx + 1).zfill(2)}-15",
                        "quarter": quarter,
                        "month": month,
                        "year": year
                    })
    
    await db.sales_data.insert_many(sales_data)
    logger.info(f"Generated {len(sales_data)} sample sales records")
    return len(sales_data)

async def perform_olap_analysis(query: Dict[str, Any]) -> Dict[str, Any]:
    """Execute OLAP operations on the sales data"""
    operation = query.get("operation", "aggregate")
    dimensions = query.get("dimensions", ["region"])
    measures = query.get("measures", ["sales_amount"])
    filters = query.get("filters", {})
    
    # Build MongoDB aggregation pipeline
    pipeline = []
    
    # Apply filters
    if filters:
        match_stage = {}
        for key, value in filters.items():
            if isinstance(value, list):
                match_stage[key] = {"$in": value}
            else:
                match_stage[key] = value
        pipeline.append({"$match": match_stage})
    
    # Group by dimensions
    group_id = {}
    for dim in dimensions:
        group_id[dim] = f"${dim}"
    
    group_stage = {"_id": group_id}
    
    # Add measures
    for measure in measures:
        group_stage[f"total_{measure}"] = {"$sum": f"${measure}"}
        group_stage[f"avg_{measure}"] = {"$avg": f"${measure}"}
        group_stage["count"] = {"$sum": 1}
    
    pipeline.append({"$group": group_stage})
    
    # Sort by total sales descending
    if "sales_amount" in measures:
        pipeline.append({"$sort": {"total_sales_amount": -1}})
    
    # Project for cleaner output
    project_stage = {"_id": 0}
    for dim in dimensions:
        project_stage[dim] = f"$_id.{dim}"
    for measure in measures:
        project_stage[f"total_{measure}"] = 1
        project_stage[f"avg_{measure}"] = {"$round": [f"$avg_{measure}", 2]}
    project_stage["count"] = 1
    
    pipeline.append({"$project": project_stage})
    
    results = await db.sales_data.aggregate(pipeline).to_list(100)
    
    return {
        "operation": operation,
        "dimensions": dimensions,
        "measures": measures,
        "filters": filters,
        "data": results,
        "row_count": len(results)
    }

# OLAP System Prompt for Claude
OLAP_SYSTEM_PROMPT = """You are an OLAP (Online Analytical Processing) Assistant that helps business users analyze sales data through natural language.

Available Data Schema:
- region: North, South, East, West, Central
- product: Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones  
- category: Electronics, Accessories, Computing
- sales_amount: Sales value in dollars
- quantity: Number of units sold
- quarter: Q1, Q2, Q3, Q4
- month: January through December
- year: 2023, 2024

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
    """Process natural language query using Claude and execute OLAP analysis"""
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    
    if not api_key:
        raise HTTPException(status_code=500, detail="LLM API key not configured")
    
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
            
            # Execute the OLAP analysis
            analysis_result = await perform_olap_analysis(query_params)
            
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
    return {"message": "OLAP Assistant API"}

@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Process natural language OLAP query"""
    session_id = request.session_id or str(uuid.uuid4())
    
    result = await process_natural_language_query(request.message, session_id)
    
    # Store message in database
    user_msg = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.chat_messages.insert_one(user_msg)
    
    assistant_msg = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "assistant",
        "content": result["response"],
        "analysis_result": result["analysis_result"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.chat_messages.insert_one(assistant_msg)
    
    return ChatResponse(
        response=result["response"],
        analysis_result=result["analysis_result"],
        session_id=session_id
    )

@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    messages = await db.chat_messages.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("timestamp", 1).to_list(100)
    return {"messages": messages}

@api_router.post("/data/init")
async def initialize_data():
    """Initialize sample sales data"""
    count = await generate_sample_data()
    return {"message": f"Sample data initialized", "record_count": count}

@api_router.get("/data/summary")
async def get_data_summary():
    """Get summary statistics of the sales data"""
    total_records = await db.sales_data.count_documents({})
    
    # Aggregate summary
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_sales": {"$sum": "$sales_amount"},
                "total_quantity": {"$sum": "$quantity"},
                "avg_sale": {"$avg": "$sales_amount"}
            }
        }
    ]
    summary = await db.sales_data.aggregate(pipeline).to_list(1)
    
    # Get unique values
    regions = await db.sales_data.distinct("region")
    products = await db.sales_data.distinct("product")
    quarters = await db.sales_data.distinct("quarter")
    years = await db.sales_data.distinct("year")
    
    return {
        "total_records": total_records,
        "total_sales": round(summary[0]["total_sales"], 2) if summary else 0,
        "total_quantity": summary[0]["total_quantity"] if summary else 0,
        "avg_sale": round(summary[0]["avg_sale"], 2) if summary else 0,
        "dimensions": {
            "regions": regions,
            "products": products,
            "quarters": quarters,
            "years": years
        }
    }

@api_router.post("/olap/query")
async def execute_olap_query(query: OLAPQuery):
    """Execute a direct OLAP query"""
    result = await perform_olap_analysis(query.model_dump())
    return result

@api_router.get("/olap/sales-by-region")
async def sales_by_region(quarter: Optional[str] = None, year: Optional[int] = None):
    """Get sales breakdown by region"""
    filters = {}
    if quarter:
        filters["quarter"] = quarter
    if year:
        filters["year"] = year
    
    result = await perform_olap_analysis({
        "operation": "aggregate",
        "dimensions": ["region"],
        "measures": ["sales_amount", "quantity"],
        "filters": filters
    })
    return result

@api_router.get("/olap/sales-by-product")
async def sales_by_product(region: Optional[str] = None, quarter: Optional[str] = None):
    """Get sales breakdown by product"""
    filters = {}
    if region:
        filters["region"] = region
    if quarter:
        filters["quarter"] = quarter
    
    result = await perform_olap_analysis({
        "operation": "aggregate",
        "dimensions": ["product"],
        "measures": ["sales_amount", "quantity"],
        "filters": filters
    })
    return result

@api_router.get("/olap/sales-by-month")
async def sales_by_month(year: Optional[int] = None, region: Optional[str] = None):
    """Get sales breakdown by month"""
    filters = {}
    if year:
        filters["year"] = year
    if region:
        filters["region"] = region
    
    result = await perform_olap_analysis({
        "operation": "aggregate",
        "dimensions": ["month", "quarter"],
        "measures": ["sales_amount", "quantity"],
        "filters": filters
    })
    return result

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
    """Initialize sample data on startup"""
    await generate_sample_data()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
