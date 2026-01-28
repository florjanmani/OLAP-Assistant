# Prompt Design Document

## Overview

This document describes the prompt engineering strategies used in the OLAP Assistant to enable natural language query processing.

---

## System Prompt

The core system prompt that guides query interpretation:

```
You are an OLAP (Online Analytical Processing) Assistant that helps business users analyze sales data through natural language.

Available Data Schema:
- region: North, South, East, West, Central
- product: Laptop, Desktop, Tablet, Phone, Monitor, Keyboard, Mouse, Headphones  
- category: Electronics, Accessories, Computing
- sales_amount: Sales value in dollars
- quantity: Number of units sold
- quarter: Q1, Q2, Q3, Q4
- month: January through December
- year: 2022, 2023, 2024

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
```

---

## Prompt Patterns

### 1. Query Classification Pattern

**Purpose**: Determine the type of analysis requested

```
Given the user query: "{query}"

Classify the intent as one of:
- NAVIGATION: Asking about data structure
- OLAP_OPERATION: Requesting data analysis
- KPI_CALCULATION: Asking for metrics/KPIs
- REPORT_GENERATION: Requesting formatted output

Return the classification with confidence score.
```

### 2. Entity Extraction Pattern

**Purpose**: Extract relevant entities from natural language

```
From the query: "{query}"

Extract the following entities:
- Dimensions mentioned (region, product, time, etc.)
- Measures requested (sales, quantity, profit)
- Filters specified (Q4, North, 2024, etc.)
- Time periods referenced
- Comparison requests

Return as structured JSON.
```

### 3. OLAP Operation Mapping Pattern

**Purpose**: Map natural language to OLAP operations

```
Map the following phrases to OLAP operations:

"drill into", "break down by", "show details" → DRILL_DOWN
"total by", "aggregate", "summarize" → ROLL_UP
"only", "just", "filter to" → SLICE
"and", "where", "both" → DICE
"compare", "versus", "side by side" → DICE/COMPARISON
"pivot", "rotate", "swap" → PIVOT
```

---

## Example Prompts and Responses

### Example 1: Drill-Down Query

**User**: "Break down Q4 sales by region"

**Expected Response**:
```json
{
    "operation": "slice",
    "dimensions": ["region"],
    "measures": ["sales_amount"],
    "filters": {"quarter": "Q4"},
    "explanation": "Filtering sales data to Q4 and grouping by region"
}
```

### Example 2: Roll-Up Query

**User**: "Show total sales by category"

**Expected Response**:
```json
{
    "operation": "roll_up",
    "dimensions": ["category"],
    "measures": ["sales_amount"],
    "filters": {},
    "explanation": "Aggregating product sales up to category level"
}
```

### Example 3: Dice Query

**User**: "Compare North and South regions in Q4"

**Expected Response**:
```json
{
    "operation": "dice",
    "dimensions": ["region"],
    "measures": ["sales_amount", "quantity"],
    "filters": {"region": ["North", "South"], "quarter": "Q4"},
    "explanation": "Filtering to North and South regions in Q4 for comparison"
}
```

### Example 4: KPI Query

**User**: "What's the year-over-year growth?"

**Expected Response**:
```json
{
    "operation": "kpi",
    "kpi_type": "yoy_growth",
    "dimensions": ["year"],
    "measures": ["sales_amount"],
    "explanation": "Calculating year-over-year sales growth"
}
```

### Example 5: Complex Query

**User**: "Drill into Q4 Electronics sales by month for the North region"

**Expected Response**:
```json
{
    "operation": "drill_down",
    "dimensions": ["month"],
    "measures": ["sales_amount"],
    "filters": {
        "quarter": "Q4",
        "category": "Electronics",
        "region": "North"
    },
    "explanation": "Drilling down from Q4 to monthly view for Electronics in North region"
}
```

---

## Prompt Templates

### Analysis Request Template

```
Analyze the following sales data query:
Query: {user_query}

Available dimensions: {dimensions}
Available measures: {measures}

Determine:
1. What OLAP operation is being requested?
2. What dimensions should be used for grouping?
3. What filters should be applied?
4. What measures should be calculated?

Provide the analysis plan in JSON format.
```

### Explanation Template

```
Based on the analysis of {measure} by {dimensions}:

Top performer: {top_item} with {top_value}
Lowest performer: {bottom_item} with {bottom_value}

The data shows {trend_description}.

Suggested next steps:
- {suggestion_1}
- {suggestion_2}
```

---

## Prompt Optimization Strategies

### 1. Few-Shot Learning
Include 3-5 examples in the prompt to guide response format.

### 2. Chain of Thought
For complex queries, break down into steps:
1. Identify operation type
2. Extract entities
3. Build query parameters
4. Generate explanation

### 3. Structured Output
Always request JSON output for reliable parsing:
```
Return your response as valid JSON with the following structure:
{
  "operation": string,
  "dimensions": array,
  "measures": array,
  "filters": object,
  "explanation": string
}
```

### 4. Error Recovery
Include fallback instructions:
```
If the query is ambiguous:
1. Make reasonable assumptions
2. Note the assumptions in the explanation
3. Suggest clarifying questions
```

---

## Validation Rules

### Dimension Validation
- Check if requested dimensions exist in schema
- Suggest alternatives if dimension not found

### Measure Validation
- Verify measures are numeric fields
- Default to sales_amount if not specified

### Filter Validation
- Validate filter values against known options
- Handle case-insensitive matching

---

## Continuous Improvement

### Logging
- Track successful and failed query interpretations
- Identify common misunderstandings

### Refinement
- Update prompts based on error patterns
- Add new examples for edge cases
- Adjust confidence thresholds
