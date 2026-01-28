"""
Cube Operations Agent
Handles OLAP cube operations: Drill-down, Roll-up, Slice, Dice, Pivot

Purpose: Execute OLAP operations on the data cube
Input: Operation type, dimensions, filters, measures
Output: Transformed data according to the operation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class OLAPOperation(Enum):
    DRILL_DOWN = "drill_down"
    ROLL_UP = "roll_up"
    SLICE = "slice"
    DICE = "dice"
    PIVOT = "pivot"
    AGGREGATE = "aggregate"


@dataclass
class CubeQuery:
    operation: OLAPOperation
    dimensions: List[str]
    measures: List[str]
    filters: Dict[str, Any]
    group_by: Optional[List[str]] = None


class CubeOperations:
    """
    Agent responsible for executing OLAP cube operations.
    
    Operations:
    - DRILL_DOWN: Navigate from summary to detail (Year → Quarter → Month)
    - ROLL_UP: Aggregate from detail to summary (Product → Category)
    - SLICE: Filter on a single dimension (Only Q4)
    - DICE: Filter on multiple dimensions (Q4 AND North region)
    - PIVOT: Rotate the cube view (swap rows/columns)
    """
    
    def __init__(self):
        self.supported_dimensions = ["region", "product", "category", "quarter", "month", "year"]
        self.supported_measures = ["sales_amount", "quantity", "profit_margin", "unit_price"]
        self.hierarchy_maps = {
            "time": ["year", "quarter", "month"],
            "product": ["category", "product"],
            "geography": ["region"]
        }
    
    def validate_query(self, query: CubeQuery) -> Dict[str, Any]:
        """Validate the cube query parameters."""
        errors = []
        
        for dim in query.dimensions:
            if dim.lower() not in self.supported_dimensions:
                errors.append(f"Unknown dimension: {dim}")
        
        for measure in query.measures:
            if measure.lower() not in self.supported_measures:
                errors.append(f"Unknown measure: {measure}")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def build_drill_down_query(self, current_level: str, target_level: str, filters: Dict) -> Dict[str, Any]:
        """
        Build a drill-down query.
        
        Example: Drill from Year=2024 to Quarters
        """
        return {
            "operation": OLAPOperation.DRILL_DOWN.value,
            "from_level": current_level,
            "to_level": target_level,
            "filters": filters,
            "description": f"Drilling down from {current_level} to {target_level}"
        }
    
    def build_roll_up_query(self, current_level: str, target_level: str, filters: Dict) -> Dict[str, Any]:
        """
        Build a roll-up query.
        
        Example: Roll up from Product to Category
        """
        return {
            "operation": OLAPOperation.ROLL_UP.value,
            "from_level": current_level,
            "to_level": target_level,
            "filters": filters,
            "description": f"Rolling up from {current_level} to {target_level}"
        }
    
    def build_slice_query(self, dimension: str, value: Any, measures: List[str]) -> Dict[str, Any]:
        """
        Build a slice query - filter on single dimension.
        
        Example: Slice on quarter='Q4'
        """
        return {
            "operation": OLAPOperation.SLICE.value,
            "slice_dimension": dimension,
            "slice_value": value,
            "measures": measures,
            "description": f"Slicing data where {dimension} = {value}"
        }
    
    def build_dice_query(self, filters: Dict[str, Any], measures: List[str]) -> Dict[str, Any]:
        """
        Build a dice query - filter on multiple dimensions.
        
        Example: Dice where quarter='Q4' AND region='North'
        """
        filter_desc = " AND ".join([f"{k}={v}" for k, v in filters.items()])
        return {
            "operation": OLAPOperation.DICE.value,
            "filters": filters,
            "measures": measures,
            "description": f"Dicing data where {filter_desc}"
        }
    
    def build_pivot_query(self, row_dims: List[str], col_dims: List[str], measures: List[str]) -> Dict[str, Any]:
        """
        Build a pivot query - rotate the view.
        
        Example: Pivot with regions as rows, quarters as columns
        """
        return {
            "operation": OLAPOperation.PIVOT.value,
            "row_dimensions": row_dims,
            "column_dimensions": col_dims,
            "measures": measures,
            "description": f"Pivoting with {row_dims} as rows and {col_dims} as columns"
        }
    
    def interpret_natural_query(self, query: str) -> Dict[str, Any]:
        """
        Interpret a natural language query and determine the OLAP operation.
        
        Examples:
        - "Drill into Q4 by month" → DRILL_DOWN
        - "Show total by category" → ROLL_UP  
        - "Only Q4 data" → SLICE
        - "Q4 in North region" → DICE
        - "Compare regions by quarter" → PIVOT
        """
        query_lower = query.lower()
        
        # Detect operation type
        if any(word in query_lower for word in ["drill", "detail", "breakdown", "by month", "by day"]):
            return {
                "detected_operation": OLAPOperation.DRILL_DOWN.value,
                "confidence": 0.85,
                "suggestion": "This appears to be a drill-down operation"
            }
        
        elif any(word in query_lower for word in ["roll up", "total", "aggregate", "by category", "summary"]):
            return {
                "detected_operation": OLAPOperation.ROLL_UP.value,
                "confidence": 0.85,
                "suggestion": "This appears to be a roll-up operation"
            }
        
        elif any(word in query_lower for word in ["only", "just", "filter"]) and query_lower.count("and") == 0:
            return {
                "detected_operation": OLAPOperation.SLICE.value,
                "confidence": 0.80,
                "suggestion": "This appears to be a slice operation (single filter)"
            }
        
        elif " and " in query_lower or ("compare" in query_lower and "between" in query_lower):
            return {
                "detected_operation": OLAPOperation.DICE.value,
                "confidence": 0.80,
                "suggestion": "This appears to be a dice operation (multiple filters)"
            }
        
        elif any(word in query_lower for word in ["pivot", "swap", "rotate", "cross-tab"]):
            return {
                "detected_operation": OLAPOperation.PIVOT.value,
                "confidence": 0.75,
                "suggestion": "This appears to be a pivot operation"
            }
        
        return {
            "detected_operation": OLAPOperation.AGGREGATE.value,
            "confidence": 0.60,
            "suggestion": "Defaulting to aggregation operation"
        }
    
    def get_operation_explanation(self, operation: str) -> Dict[str, str]:
        """Return a detailed explanation of an OLAP operation."""
        explanations = {
            "drill_down": {
                "name": "Drill-Down",
                "description": "Navigate from summary to detailed data by moving down the hierarchy.",
                "example": "Year → Quarter → Month → Day",
                "use_case": "When you want to see more granular details"
            },
            "roll_up": {
                "name": "Roll-Up",
                "description": "Aggregate data by moving up the hierarchy from detailed to summary.",
                "example": "Product → Category → All Products",
                "use_case": "When you want to see the bigger picture"
            },
            "slice": {
                "name": "Slice",
                "description": "Select a single dimension value to create a sub-cube of data.",
                "example": "Filter by Quarter = 'Q4'",
                "use_case": "When you want to focus on one specific value"
            },
            "dice": {
                "name": "Dice",
                "description": "Select multiple dimension values to create a sub-cube.",
                "example": "Region IN ('North', 'South') AND Quarter = 'Q4'",
                "use_case": "When you need multiple filters simultaneously"
            },
            "pivot": {
                "name": "Pivot",
                "description": "Rotate the data cube to view data from different perspectives.",
                "example": "Swap rows and columns in the view",
                "use_case": "When you want to see data from a different angle"
            }
        }
        return explanations.get(operation, {"error": "Unknown operation"})


# Singleton instance
cube_operations = CubeOperations()
