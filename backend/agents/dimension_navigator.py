"""
Dimension Navigator Agent
Handles navigation through data dimensions and hierarchies.

Purpose: Navigate the multidimensional data structure
Input: User queries about dimensions, hierarchies, available data
Output: Dimension information, hierarchy paths, navigation suggestions
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class DimensionType(Enum):
    TIME = "time"
    GEOGRAPHY = "geography"
    PRODUCT = "product"
    CATEGORY = "category"


@dataclass
class Dimension:
    name: str
    type: DimensionType
    hierarchy: List[str]
    values: List[str]


class DimensionNavigator:
    """
    Agent responsible for navigating through OLAP dimensions.
    
    Capabilities:
    - List available dimensions
    - Show dimension hierarchies
    - Navigate up/down hierarchies
    - Suggest related dimensions
    """
    
    def __init__(self):
        self.dimensions = self._initialize_dimensions()
    
    def _initialize_dimensions(self) -> Dict[str, Dimension]:
        """Initialize the dimension metadata."""
        return {
            "time": Dimension(
                name="Time",
                type=DimensionType.TIME,
                hierarchy=["Year", "Quarter", "Month", "Day"],
                values=["2022", "2023", "2024"]
            ),
            "geography": Dimension(
                name="Geography",
                type=DimensionType.GEOGRAPHY,
                hierarchy=["Region"],
                values=["North", "South", "East", "West", "Central"]
            ),
            "product": Dimension(
                name="Product",
                type=DimensionType.PRODUCT,
                hierarchy=["Category", "Product"],
                values=["Laptop", "Desktop", "Tablet", "Phone", "Monitor", "Keyboard", "Mouse", "Headphones"]
            )
        }
    
    def get_all_dimensions(self) -> List[Dict[str, Any]]:
        """Return all available dimensions with their metadata."""
        return [
            {
                "name": dim.name,
                "type": dim.type.value,
                "hierarchy": dim.hierarchy,
                "values_count": len(dim.values)
            }
            for dim in self.dimensions.values()
        ]
    
    def get_dimension_hierarchy(self, dimension_name: str) -> Optional[List[str]]:
        """Get the hierarchy levels for a specific dimension."""
        dim = self.dimensions.get(dimension_name.lower())
        return dim.hierarchy if dim else None
    
    def get_dimension_values(self, dimension_name: str) -> Optional[List[str]]:
        """Get all possible values for a dimension."""
        dim = self.dimensions.get(dimension_name.lower())
        return dim.values if dim else None
    
    def suggest_drill_path(self, current_dimension: str, current_level: str) -> Dict[str, Any]:
        """Suggest next drill-down or roll-up paths."""
        dim = self.dimensions.get(current_dimension.lower())
        if not dim:
            return {"error": f"Dimension '{current_dimension}' not found"}
        
        hierarchy = dim.hierarchy
        try:
            current_idx = hierarchy.index(current_level)
            suggestions = {
                "current_level": current_level,
                "can_drill_down": current_idx < len(hierarchy) - 1,
                "can_roll_up": current_idx > 0
            }
            
            if suggestions["can_drill_down"]:
                suggestions["drill_down_to"] = hierarchy[current_idx + 1]
            if suggestions["can_roll_up"]:
                suggestions["roll_up_to"] = hierarchy[current_idx - 1]
            
            return suggestions
        except ValueError:
            return {"error": f"Level '{current_level}' not found in dimension"}
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query about dimensions.
        
        Examples:
        - "What dimensions are available?"
        - "Show me the time hierarchy"
        - "What products exist?"
        """
        query_lower = query.lower()
        
        if "available" in query_lower or "all dimension" in query_lower:
            return {
                "action": "list_dimensions",
                "result": self.get_all_dimensions()
            }
        
        for dim_name in self.dimensions.keys():
            if dim_name in query_lower:
                if "hierarchy" in query_lower:
                    return {
                        "action": "get_hierarchy",
                        "dimension": dim_name,
                        "result": self.get_dimension_hierarchy(dim_name)
                    }
                elif "values" in query_lower or "what" in query_lower:
                    return {
                        "action": "get_values",
                        "dimension": dim_name,
                        "result": self.get_dimension_values(dim_name)
                    }
        
        return {
            "action": "unknown",
            "message": "Could not understand the dimension query",
            "available_dimensions": list(self.dimensions.keys())
        }


# Singleton instance
dimension_navigator = DimensionNavigator()
