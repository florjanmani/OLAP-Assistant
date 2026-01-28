"""
Report Generator Agent
Generates formatted reports and visualizations from analysis results.

Purpose: Create human-readable reports and export formats
Input: Analysis results, report type, format preferences
Output: Formatted reports in various formats (text, JSON, HTML)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class ReportFormat(Enum):
    TEXT = "text"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"


class ReportType(Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    COMPARISON = "comparison"
    TREND = "trend"
    KPI = "kpi"


@dataclass
class ReportConfig:
    report_type: ReportType
    format: ReportFormat
    include_charts: bool
    include_recommendations: bool
    title: str


class ReportGenerator:
    """
    Agent responsible for generating formatted reports.
    
    Capabilities:
    - Generate summary reports
    - Create detailed analysis reports
    - Format comparison reports
    - Produce trend analysis reports
    - Generate KPI dashboards
    """
    
    def __init__(self):
        self.report_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize report templates."""
        return {
            "summary": """
# {title}
Generated: {timestamp}

## Overview
{overview}

## Key Metrics
{metrics}

## Highlights
{highlights}
""",
            "detailed": """
# {title}
Generated: {timestamp}

## Executive Summary
{summary}

## Detailed Analysis
{analysis}

## Data Tables
{tables}

## Recommendations
{recommendations}
""",
            "comparison": """
# {title}
Generated: {timestamp}

## Comparison Overview
{overview}

## Side-by-Side Analysis
{comparison_data}

## Key Differences
{differences}

## Insights
{insights}
"""
        }
    
    def generate_summary_report(self, data: Dict[str, Any], title: str = "OLAP Analysis Report") -> str:
        """Generate a summary report in markdown format."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract key information
        operation = data.get("operation", "analysis")
        dimensions = data.get("dimensions", [])
        filters = data.get("filters", {})
        results = data.get("data", [])
        row_count = data.get("row_count", len(results))
        
        # Build overview
        overview = f"""
- **Operation**: {operation.replace('_', ' ').title()}
- **Dimensions Analyzed**: {', '.join(dimensions) if dimensions else 'N/A'}
- **Filters Applied**: {', '.join([f'{k}={v}' for k,v in filters.items()]) if filters else 'None'}
- **Results Count**: {row_count} rows
"""
        
        # Build metrics section
        if results:
            total_sales = sum(r.get("total_sales_amount", 0) for r in results)
            total_quantity = sum(r.get("total_quantity", 0) for r in results)
            metrics = f"""
| Metric | Value |
|--------|-------|
| Total Sales | ${total_sales:,.2f} |
| Total Quantity | {total_quantity:,} |
| Average per Group | ${total_sales/row_count:,.2f} |
"""
        else:
            metrics = "No data available for metrics calculation."
        
        # Build highlights
        if results and len(results) > 0:
            # Find top performer
            top = max(results, key=lambda x: x.get("total_sales_amount", 0))
            top_name = list(top.values())[0] if top else "N/A"
            top_value = top.get("total_sales_amount", 0)
            
            highlights = f"""
- **Top Performer**: {top_name} with ${top_value:,.2f} in sales
- **Number of Groups**: {row_count}
"""
        else:
            highlights = "No highlights available."
        
        report = self.report_templates["summary"].format(
            title=title,
            timestamp=timestamp,
            overview=overview,
            metrics=metrics,
            highlights=highlights
        )
        
        return report
    
    def generate_comparison_report(self, data1: Dict, data2: Dict, labels: List[str]) -> str:
        """Generate a comparison report between two datasets."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        label1, label2 = labels if len(labels) >= 2 else ["Dataset 1", "Dataset 2"]
        
        # Calculate totals
        total1 = sum(r.get("total_sales_amount", 0) for r in data1.get("data", []))
        total2 = sum(r.get("total_sales_amount", 0) for r in data2.get("data", []))
        
        qty1 = sum(r.get("total_quantity", 0) for r in data1.get("data", []))
        qty2 = sum(r.get("total_quantity", 0) for r in data2.get("data", []))
        
        comparison_data = f"""
| Metric | {label1} | {label2} | Difference |
|--------|----------|----------|------------|
| Total Sales | ${total1:,.2f} | ${total2:,.2f} | ${total1-total2:,.2f} |
| Total Quantity | {qty1:,} | {qty2:,} | {qty1-qty2:,} |
"""
        
        # Calculate percentage difference
        if total2 > 0:
            pct_diff = ((total1 - total2) / total2) * 100
            winner = label1 if total1 > total2 else label2
            diff_text = f"{abs(pct_diff):.1f}% {'higher' if pct_diff > 0 else 'lower'}"
        else:
            diff_text = "N/A"
            winner = label1
        
        differences = f"""
- **Sales Leader**: {winner}
- **Difference**: {label1} is {diff_text} than {label2}
"""
        
        insights = f"""
Based on the comparison:
- {winner} shows stronger performance in total sales
- Consider investigating factors contributing to the difference
- Look for opportunities to replicate success across both groups
"""
        
        report = self.report_templates["comparison"].format(
            title=f"Comparison: {label1} vs {label2}",
            timestamp=timestamp,
            overview=f"Comparing {label1} and {label2} performance metrics.",
            comparison_data=comparison_data,
            differences=differences,
            insights=insights
        )
        
        return report
    
    def generate_kpi_report(self, kpi_data: Dict[str, Any]) -> str:
        """Generate a KPI-focused report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# KPI Dashboard Report
Generated: {timestamp}

## Key Performance Indicators

| KPI | Value | Status |
|-----|-------|--------|
"""
        
        # Add KPIs to table
        if "total_revenue" in kpi_data:
            report += f"| Total Revenue | ${kpi_data['total_revenue']:,.2f} | ✓ |\n"
        
        if "total_units_sold" in kpi_data:
            report += f"| Units Sold | {kpi_data['total_units_sold']:,} | ✓ |\n"
        
        if "average_order_value" in kpi_data:
            report += f"| Avg Order Value | ${kpi_data['average_order_value']:,.2f} | ✓ |\n"
        
        if "average_profit_margin" in kpi_data:
            margin = kpi_data['average_profit_margin']
            status = "✓" if margin > 20 else "⚠"
            report += f"| Profit Margin | {margin:.1f}% | {status} |\n"
        
        if "num_transactions" in kpi_data:
            report += f"| Transactions | {kpi_data['num_transactions']:,} | ✓ |\n"
        
        return report
    
    def format_data_table(self, data: List[Dict], max_rows: int = 10) -> str:
        """Format data as a markdown table."""
        if not data:
            return "No data available."
        
        # Get headers from first row
        headers = list(data[0].keys())
        
        # Build table
        table = "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        for row in data[:max_rows]:
            values = []
            for h in headers:
                v = row.get(h, "")
                if isinstance(v, float):
                    v = f"{v:,.2f}"
                elif isinstance(v, int):
                    v = f"{v:,}"
                values.append(str(v))
            table += "| " + " | ".join(values) + " |\n"
        
        if len(data) > max_rows:
            table += f"\n*Showing {max_rows} of {len(data)} rows*\n"
        
        return table
    
    def generate_natural_language_summary(self, analysis_result: Dict) -> str:
        """Generate a natural language summary of analysis results."""
        operation = analysis_result.get("operation", "analysis")
        dimensions = analysis_result.get("dimensions", [])
        data = analysis_result.get("data", [])
        filters = analysis_result.get("filters", {})
        
        if not data:
            return "No data was returned from the analysis."
        
        # Find top and bottom performers
        if data:
            sorted_data = sorted(data, key=lambda x: x.get("total_sales_amount", 0), reverse=True)
            top = sorted_data[0]
            bottom = sorted_data[-1]
            
            # Get the dimension value (first non-numeric field)
            dim_key = dimensions[0] if dimensions else list(top.keys())[0]
            top_name = top.get(dim_key, "Top performer")
            bottom_name = bottom.get(dim_key, "Bottom performer")
            top_value = top.get("total_sales_amount", 0)
            bottom_value = bottom.get("total_sales_amount", 0)
            
            total = sum(r.get("total_sales_amount", 0) for r in data)
            avg = total / len(data)
            
            summary = f"""
Based on the {operation.replace('_', ' ')} analysis across {', '.join(dimensions)}:

**Top Performer**: {top_name} leads with ${top_value:,.2f} in sales
**Lowest Performer**: {bottom_name} has ${bottom_value:,.2f} in sales
**Total across all groups**: ${total:,.2f}
**Average per group**: ${avg:,.2f}

The top performer generates {(top_value/total)*100:.1f}% of total sales in this view.
"""
            
            if filters:
                filter_str = ', '.join([f"{k}={v}" for k,v in filters.items()])
                summary += f"\n*Filters applied: {filter_str}*"
            
            return summary
        
        return "Analysis complete. Please review the data for insights."
    
    def export_to_json(self, data: Dict[str, Any]) -> str:
        """Export analysis results to JSON format."""
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "analysis": data
        }
        return json.dumps(export_data, indent=2, default=str)


# Singleton instance
report_generator = ReportGenerator()
