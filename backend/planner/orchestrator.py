"""
OLAP Orchestrator
Coordinates between specialized agents to process user queries.

Purpose: Route queries to appropriate agents and combine results
Input: Natural language queries from users
Output: Coordinated responses from multiple agents
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import re

# Import agents
from backend.agents.dimension_navigator import dimension_navigator
from backend.agents.cube_operations import cube_operations
from backend.agents.kpi_calculator import kpi_calculator
from backend.agents.report_generator import report_generator


class QueryIntent(Enum):
    NAVIGATION = "navigation"       # Questions about dimensions/structure
    OLAP_OPERATION = "olap"         # Drill-down, roll-up, slice, dice, pivot
    KPI_CALCULATION = "kpi"         # Growth rates, margins, averages
    REPORT_GENERATION = "report"    # Export, summary, format requests
    GENERAL_ANALYSIS = "analysis"   # General queries


class Orchestrator:
    """
    Central coordinator for the OLAP Assistant.
    
    Responsibilities:
    - Classify incoming queries by intent
    - Route queries to appropriate agents
    - Combine results from multiple agents
    - Provide unified responses
    """
    
    def __init__(self):
        self.agents = {
            "dimension_navigator": dimension_navigator,
            "cube_operations": cube_operations,
            "kpi_calculator": kpi_calculator,
            "report_generator": report_generator
        }
        
        # Intent classification patterns
        self.intent_patterns = {
            QueryIntent.NAVIGATION: [
                r"what dimension",
                r"show.*hierarchy",
                r"available.*dimension",
                r"what.*values",
                r"list.*dimension"
            ],
            QueryIntent.KPI_CALCULATION: [
                r"growth",
                r"yoy|mom|qoq",
                r"year.over.year",
                r"margin",
                r"average.*order",
                r"kpi",
                r"performance"
            ],
            QueryIntent.REPORT_GENERATION: [
                r"export",
                r"report",
                r"summary",
                r"pdf",
                r"download"
            ],
            QueryIntent.OLAP_OPERATION: [
                r"drill",
                r"roll.up",
                r"slice",
                r"dice",
                r"pivot",
                r"break.*down",
                r"by region",
                r"by product",
                r"by month",
                r"compare",
                r"filter",
                r"only.*q[1-4]",
                r"total.*by"
            ]
        }
    
    def classify_intent(self, query: str) -> QueryIntent:
        """Classify the user's query intent."""
        query_lower = query.lower()
        
        # Check each intent's patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        # Default to general analysis
        return QueryIntent.GENERAL_ANALYSIS
    
    def extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract relevant entities from the query."""
        query_lower = query.lower()
        entities = {
            "dimensions": [],
            "measures": [],
            "filters": {},
            "time_period": None
        }
        
        # Extract dimensions
        dimension_keywords = {
            "region": ["region", "regions", "geographic", "area"],
            "product": ["product", "products", "item"],
            "category": ["category", "categories"],
            "quarter": ["quarter", "quarters", "q1", "q2", "q3", "q4"],
            "month": ["month", "months", "monthly"],
            "year": ["year", "years", "yearly", "2022", "2023", "2024"]
        }
        
        for dim, keywords in dimension_keywords.items():
            if any(kw in query_lower for kw in keywords):
                entities["dimensions"].append(dim)
        
        # Extract filters
        quarter_match = re.search(r'q([1-4])', query_lower)
        if quarter_match:
            entities["filters"]["quarter"] = f"Q{quarter_match.group(1)}"
        
        year_match = re.search(r'(202[2-4])', query_lower)
        if year_match:
            entities["filters"]["year"] = int(year_match.group(1))
        
        region_keywords = ["north", "south", "east", "west", "central"]
        for region in region_keywords:
            if region in query_lower:
                entities["filters"]["region"] = region.capitalize()
        
        # Extract measures
        if any(word in query_lower for word in ["sales", "revenue", "amount"]):
            entities["measures"].append("sales_amount")
        if any(word in query_lower for word in ["quantity", "units", "count"]):
            entities["measures"].append("quantity")
        if any(word in query_lower for word in ["margin", "profit"]):
            entities["measures"].append("profit_margin")
        
        # Default measure if none specified
        if not entities["measures"]:
            entities["measures"] = ["sales_amount"]
        
        return entities
    
    def route_query(self, query: str, data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Route the query to appropriate agent(s) and return combined result."""
        intent = self.classify_intent(query)
        entities = self.extract_entities(query)
        
        response = {
            "query": query,
            "intent": intent.value,
            "entities": entities,
            "agents_used": [],
            "result": None
        }
        
        try:
            if intent == QueryIntent.NAVIGATION:
                result = self.agents["dimension_navigator"].process_query(query)
                response["agents_used"].append("dimension_navigator")
                response["result"] = result
            
            elif intent == QueryIntent.KPI_CALCULATION:
                if data:
                    result = self.agents["kpi_calculator"].process_kpi_query(query, data)
                else:
                    result = {"message": "KPI calculation requires data"}
                response["agents_used"].append("kpi_calculator")
                response["result"] = result
            
            elif intent == QueryIntent.REPORT_GENERATION:
                if data:
                    report = self.agents["report_generator"].generate_summary_report(
                        {"data": data, "dimensions": entities["dimensions"]},
                        title="Analysis Report"
                    )
                    result = {"report": report}
                else:
                    result = {"message": "Report generation requires data"}
                response["agents_used"].append("report_generator")
                response["result"] = result
            
            elif intent == QueryIntent.OLAP_OPERATION:
                # Determine specific OLAP operation
                operation_info = self.agents["cube_operations"].interpret_natural_query(query)
                response["agents_used"].append("cube_operations")
                
                # Build the query parameters
                result = {
                    "operation": operation_info["detected_operation"],
                    "dimensions": entities["dimensions"] or ["region"],
                    "measures": entities["measures"],
                    "filters": entities["filters"],
                    "operation_details": operation_info
                }
                response["result"] = result
            
            else:  # GENERAL_ANALYSIS
                # Use cube operations for general queries
                operation_info = self.agents["cube_operations"].interpret_natural_query(query)
                response["agents_used"].append("cube_operations")
                response["result"] = {
                    "operation": operation_info["detected_operation"],
                    "dimensions": entities["dimensions"] or ["region"],
                    "measures": entities["measures"],
                    "filters": entities["filters"]
                }
        
        except Exception as e:
            response["error"] = str(e)
        
        return response
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get the status of all agents."""
        return {
            "dimension_navigator": "active",
            "cube_operations": "active",
            "kpi_calculator": "active",
            "report_generator": "active"
        }
    
    def get_capabilities(self) -> Dict[str, List[str]]:
        """Return the capabilities of each agent."""
        return {
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
            "kpi_calculator": [
                "Year-over-Year growth",
                "Quarter-over-Quarter growth",
                "Profit margin calculation",
                "Average order value",
                "KPI summaries"
            ],
            "report_generator": [
                "Summary reports",
                "Comparison reports",
                "KPI dashboards",
                "Data table formatting",
                "Natural language summaries"
            ]
        }


# Singleton instance
orchestrator = Orchestrator()
