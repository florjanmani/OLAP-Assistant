"""
KPI Calculator Agent
Calculates Key Performance Indicators and business metrics.

Purpose: Compute KPIs, growth rates, and analytical metrics
Input: Data, KPI type, time periods for comparison
Output: Calculated KPIs with interpretations
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class KPIType(Enum):
    YOY_GROWTH = "yoy_growth"           # Year-over-Year Growth
    MOM_GROWTH = "mom_growth"           # Month-over-Month Growth
    QOQ_GROWTH = "qoq_growth"           # Quarter-over-Quarter Growth
    PROFIT_MARGIN = "profit_margin"      # Profit Margin %
    AVERAGE_ORDER = "average_order"      # Average Order Value
    TOTAL_REVENUE = "total_revenue"      # Total Revenue
    TOTAL_UNITS = "total_units"          # Total Units Sold
    REVENUE_PER_UNIT = "revenue_per_unit"  # Revenue per Unit


@dataclass
class KPIResult:
    kpi_type: KPIType
    value: float
    formatted_value: str
    comparison_value: Optional[float]
    change_percentage: Optional[float]
    interpretation: str


class KPICalculator:
    """
    Agent responsible for calculating Key Performance Indicators.
    
    Capabilities:
    - Calculate growth rates (YoY, MoM, QoQ)
    - Compute profit margins
    - Calculate average order values
    - Generate KPI interpretations
    """
    
    def __init__(self):
        self.kpi_definitions = self._initialize_kpi_definitions()
    
    def _initialize_kpi_definitions(self) -> Dict[str, Dict]:
        """Initialize KPI metadata and calculation rules."""
        return {
            "yoy_growth": {
                "name": "Year-over-Year Growth",
                "formula": "((Current Year - Previous Year) / Previous Year) × 100",
                "unit": "%",
                "positive_is_good": True
            },
            "mom_growth": {
                "name": "Month-over-Month Growth",
                "formula": "((Current Month - Previous Month) / Previous Month) × 100",
                "unit": "%",
                "positive_is_good": True
            },
            "qoq_growth": {
                "name": "Quarter-over-Quarter Growth",
                "formula": "((Current Quarter - Previous Quarter) / Previous Quarter) × 100",
                "unit": "%",
                "positive_is_good": True
            },
            "profit_margin": {
                "name": "Profit Margin",
                "formula": "(Profit / Revenue) × 100",
                "unit": "%",
                "positive_is_good": True
            },
            "average_order": {
                "name": "Average Order Value",
                "formula": "Total Revenue / Number of Orders",
                "unit": "$",
                "positive_is_good": True
            }
        }
    
    def calculate_growth_rate(self, current_value: float, previous_value: float) -> Dict[str, Any]:
        """Calculate growth rate between two values."""
        if previous_value == 0:
            return {
                "growth_rate": None,
                "error": "Cannot calculate growth rate: previous value is zero"
            }
        
        growth_rate = ((current_value - previous_value) / previous_value) * 100
        
        return {
            "current_value": current_value,
            "previous_value": previous_value,
            "growth_rate": round(growth_rate, 2),
            "absolute_change": round(current_value - previous_value, 2),
            "interpretation": self._interpret_growth(growth_rate)
        }
    
    def _interpret_growth(self, growth_rate: float) -> str:
        """Generate human-readable interpretation of growth rate."""
        if growth_rate > 20:
            return "Exceptional growth - significantly exceeding expectations"
        elif growth_rate > 10:
            return "Strong growth - performing well above average"
        elif growth_rate > 5:
            return "Healthy growth - meeting expectations"
        elif growth_rate > 0:
            return "Modest growth - slight improvement"
        elif growth_rate > -5:
            return "Slight decline - minor concern"
        elif growth_rate > -10:
            return "Moderate decline - requires attention"
        else:
            return "Significant decline - immediate action needed"
    
    def calculate_yoy_growth(self, data: List[Dict], measure: str = "sales_amount") -> Dict[str, Any]:
        """Calculate Year-over-Year growth."""
        yearly_totals = {}
        
        for record in data:
            year = record.get("year")
            value = record.get(measure, 0)
            yearly_totals[year] = yearly_totals.get(year, 0) + value
        
        years = sorted(yearly_totals.keys())
        if len(years) < 2:
            return {"error": "Need at least 2 years of data for YoY calculation"}
        
        results = []
        for i in range(1, len(years)):
            current_year = years[i]
            previous_year = years[i-1]
            
            growth = self.calculate_growth_rate(
                yearly_totals[current_year],
                yearly_totals[previous_year]
            )
            growth["year"] = current_year
            growth["comparison_year"] = previous_year
            results.append(growth)
        
        return {
            "kpi_type": "yoy_growth",
            "measure": measure,
            "results": results,
            "yearly_totals": yearly_totals
        }
    
    def calculate_qoq_growth(self, data: List[Dict], year: int, measure: str = "sales_amount") -> Dict[str, Any]:
        """Calculate Quarter-over-Quarter growth for a specific year."""
        quarterly_totals = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
        
        for record in data:
            if record.get("year") == year:
                quarter = record.get("quarter")
                value = record.get(measure, 0)
                quarterly_totals[quarter] = quarterly_totals.get(quarter, 0) + value
        
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        results = []
        
        for i in range(1, len(quarters)):
            current_q = quarters[i]
            previous_q = quarters[i-1]
            
            if quarterly_totals[previous_q] > 0:
                growth = self.calculate_growth_rate(
                    quarterly_totals[current_q],
                    quarterly_totals[previous_q]
                )
                growth["quarter"] = current_q
                growth["comparison_quarter"] = previous_q
                results.append(growth)
        
        return {
            "kpi_type": "qoq_growth",
            "year": year,
            "measure": measure,
            "results": results,
            "quarterly_totals": quarterly_totals
        }
    
    def calculate_profit_margin(self, revenue: float, cost: float) -> Dict[str, Any]:
        """Calculate profit margin percentage."""
        if revenue == 0:
            return {"error": "Cannot calculate margin: revenue is zero"}
        
        profit = revenue - cost
        margin = (profit / revenue) * 100
        
        return {
            "kpi_type": "profit_margin",
            "revenue": revenue,
            "cost": cost,
            "profit": round(profit, 2),
            "margin_percentage": round(margin, 2),
            "interpretation": self._interpret_margin(margin)
        }
    
    def _interpret_margin(self, margin: float) -> str:
        """Interpret profit margin."""
        if margin > 40:
            return "Excellent margin - highly profitable"
        elif margin > 25:
            return "Good margin - healthy profitability"
        elif margin > 15:
            return "Average margin - acceptable profitability"
        elif margin > 5:
            return "Low margin - consider cost optimization"
        else:
            return "Very low/negative margin - urgent attention needed"
    
    def calculate_average_order_value(self, total_revenue: float, num_orders: int) -> Dict[str, Any]:
        """Calculate average order value (AOV)."""
        if num_orders == 0:
            return {"error": "Cannot calculate AOV: no orders"}
        
        aov = total_revenue / num_orders
        
        return {
            "kpi_type": "average_order_value",
            "total_revenue": round(total_revenue, 2),
            "num_orders": num_orders,
            "aov": round(aov, 2),
            "formatted": f"${aov:,.2f}"
        }
    
    def get_kpi_summary(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate a comprehensive KPI summary from the data."""
        total_revenue = sum(r.get("sales_amount", 0) for r in data)
        total_quantity = sum(r.get("quantity", 0) for r in data)
        num_transactions = len(data)
        
        # Calculate average profit margin
        margins = [r.get("profit_margin", 0.25) for r in data if "profit_margin" in r]
        avg_margin = sum(margins) / len(margins) if margins else 0.25
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_revenue_formatted": f"${total_revenue:,.2f}",
            "total_units_sold": total_quantity,
            "num_transactions": num_transactions,
            "average_order_value": round(total_revenue / num_transactions, 2) if num_transactions > 0 else 0,
            "average_profit_margin": round(avg_margin * 100, 2),
            "revenue_per_unit": round(total_revenue / total_quantity, 2) if total_quantity > 0 else 0
        }
    
    def process_kpi_query(self, query: str, data: List[Dict]) -> Dict[str, Any]:
        """Process a natural language KPI query."""
        query_lower = query.lower()
        
        if "yoy" in query_lower or "year over year" in query_lower or "yearly growth" in query_lower:
            return self.calculate_yoy_growth(data)
        
        elif "qoq" in query_lower or "quarter over quarter" in query_lower or "quarterly growth" in query_lower:
            # Default to most recent year
            years = list(set(r.get("year") for r in data))
            latest_year = max(years) if years else 2024
            return self.calculate_qoq_growth(data, latest_year)
        
        elif "margin" in query_lower or "profit" in query_lower:
            total_revenue = sum(r.get("sales_amount", 0) for r in data)
            # Estimate cost as 70% of revenue (30% margin)
            estimated_cost = total_revenue * 0.70
            return self.calculate_profit_margin(total_revenue, estimated_cost)
        
        elif "average" in query_lower and "order" in query_lower:
            total_revenue = sum(r.get("sales_amount", 0) for r in data)
            return self.calculate_average_order_value(total_revenue, len(data))
        
        else:
            return self.get_kpi_summary(data)


# Singleton instance
kpi_calculator = KPICalculator()
