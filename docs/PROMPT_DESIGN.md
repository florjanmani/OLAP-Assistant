# Prompt Design Document

## Overview

This document details the prompt engineering approach used in the OLAP Assistant to transform natural language queries into structured OLAP operations. The system leverages a Large Language Model (LLM) with carefully crafted prompts to understand user intent and generate executable query parameters.

---

## System Prompt Architecture

### Primary System Prompt

The main system prompt establishes the LLM's role, provides context about the data schema, defines available operations, and specifies the expected output format.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SYSTEM PROMPT STRUCTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│  1. Role Definition                                                  │
│     └── Establishes the AI as an OLAP Assistant                     │
│                                                                      │
│  2. Data Schema Description                                          │
│     └── Dimensions, measures, and their possible values             │
│                                                                      │
│  3. OLAP Operations Reference                                        │
│     └── Definitions of drill-down, roll-up, slice, dice, pivot      │
│                                                                      │
│  4. Output Format Specification                                      │
│     └── JSON schema for structured responses                        │
│                                                                      │
│  5. Example Queries and Responses                                    │
│     └── Few-shot learning examples                                  │
│                                                                      │
│  6. Response Guidelines                                              │
│     └── Instructions for generating explanations                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Complete System Prompt

```python
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
```

---

## Prompt Design Principles

### 1. Role Definition (Identity Priming)

**Purpose:** Establish the AI's expertise and behavioral expectations.

```
"You are an OLAP (Online Analytical Processing) Assistant that helps 
business users analyze sales data through natural language."
```

**Key elements:**
- Specific domain expertise (OLAP)
- Target audience (business users)
- Primary capability (natural language analysis)

### 2. Schema Grounding

**Purpose:** Provide complete context about the data structure to prevent hallucination.

```
Available Data Schema (Star Schema):
- Dimensions: region, product, category, quarter, month, year
- Measures: sales_amount, quantity, profit_margin
- Regions: North, South, East, West, Central
- Products: [list of 8 products]
- Categories: Electronics, Accessories, Computing
- Time: Years 2022-2024, Quarters Q1-Q4, Months January-December
```

**Design choices:**
- Explicit listing of all valid values
- Star schema terminology for consistency
- Hierarchical relationships implied in structure

### 3. Operation Definitions

**Purpose:** Define the vocabulary for OLAP operations with clear examples.

```
OLAP Operations You Can Perform:
1. DRILL-DOWN: Go from summary to detail (e.g., Year → Quarter → Month)
2. ROLL-UP: Aggregate from detail to summary (e.g., Product → Category)
3. SLICE: Filter data on one dimension (e.g., only Q4)
4. DICE: Filter on multiple dimensions (e.g., Q4 AND North region)
5. PIVOT: Rotate dimensions for different views
```

**Design choices:**
- Numbered list for clarity
- Each operation has a brief definition
- Concrete examples in parentheses
- Uses common OLAP terminology

### 4. Output Format Specification

**Purpose:** Ensure consistent, parseable JSON output.

```json
{
    "operation": "drill_down|roll_up|slice|dice|pivot|aggregate",
    "dimensions": ["list of dimensions to group by"],
    "measures": ["sales_amount", "quantity"],
    "filters": {"dimension": "value or [values]"},
    "explanation": "Brief explanation of what analysis you're performing"
}
```

**Design choices:**
- Strict JSON schema
- Enum for operation types
- Flexible filter structure (single value or array)
- Required explanation field for user-friendly output

### 5. Few-Shot Examples

**Purpose:** Demonstrate expected behavior through concrete examples.

| User Query | Expected Output |
|------------|-----------------|
| "Show Q4 sales by region" | `{"operation": "slice", "dimensions": ["region"], "measures": ["sales_amount"], "filters": {"quarter": "Q4"}}` |
| "Drill into North region by month" | `{"operation": "drill_down", "dimensions": ["month"], "measures": ["sales_amount"], "filters": {"region": "North"}}` |
| "What's the total sales by category?" | `{"operation": "aggregate", "dimensions": ["category"], "measures": ["sales_amount"], "filters": {}}` |

**Design choices:**
- 3 examples covering different operations
- Variety in query phrasing
- Shows both filtered and unfiltered queries
- Demonstrates different dimension combinations

---

## Query Type Mapping

### Natural Language to Operation

| User Intent Pattern | OLAP Operation | Example Query |
|---------------------|----------------|---------------|
| "by month", "by day", "detail", "breakdown" | DRILL_DOWN | "Break down Q4 sales by month" |
| "total", "overall", "by category" | ROLL_UP | "Show total sales by category" |
| "only", "just", "filter to" (single) | SLICE | "Show only Q4 data" |
| "and", "compare X and Y" | DICE | "Q4 sales in North and South" |
| "pivot", "swap", "rotate" | PIVOT | "Pivot by region vs quarter" |
| "show", "what is", (default) | AGGREGATE | "What are sales by region?" |

### Dimension Detection

| Keywords | Detected Dimension |
|----------|-------------------|
| "region", "area", "geographic", "north/south/east/west" | region |
| "product", "item", "laptop/phone/etc" | product |
| "category", "type", "electronics/computing" | category |
| "quarter", "Q1/Q2/Q3/Q4" | quarter |
| "month", "January/February/etc" | month |
| "year", "2022/2023/2024" | year |

### Measure Detection

| Keywords | Detected Measure |
|----------|-----------------|
| "sales", "revenue", "amount" | sales_amount |
| "quantity", "units", "count", "volume" | quantity |
| "margin", "profit" | profit_margin |

---

## Response Processing

### JSON Extraction

The system extracts the JSON object from the LLM response:

```python
def extract_json(response: str) -> dict:
    json_start = response.find('{')
    json_end = response.rfind('}') + 1
    
    if json_start != -1 and json_end > json_start:
        json_str = response[json_start:json_end]
        return json.loads(json_str)
    return None
```

### Response Structure

```
┌─────────────────────────────────────────┐
│           LLM Response                   │
├─────────────────────────────────────────┤
│ {                                        │
│   "operation": "slice",                  │
│   "dimensions": ["region"],              │   ← JSON Object
│   "measures": ["sales_amount"],          │     (parsed)
│   "filters": {"quarter": "Q4"},          │
│   "explanation": "Filtering to Q4..."    │
│ }                                        │
├─────────────────────────────────────────┤
│ Additional explanation text for the      │   ← Natural Language
│ business user about what this means...   │     (displayed to user)
└─────────────────────────────────────────┘
```

---

## Prompt Optimization Strategies

### 1. Clarity Over Brevity

The prompt explicitly lists all options rather than using abbreviations:
- Lists all 5 regions by name
- Lists all 8 products by name
- Lists all operation types with definitions

### 2. Structured Output Enforcement

- JSON schema is explicitly defined
- Field names are consistent with backend expectations
- Examples demonstrate exact format

### 3. Graceful Degradation

Default behavior when query is ambiguous:
```python
# Default to AGGREGATE if operation unclear
"operation": "aggregate"

# Default to region if dimension unclear
"dimensions": ["region"]

# Default to sales_amount if measure unclear
"measures": ["sales_amount"]
```

### 4. Context Preservation

The system prompt includes:
- Complete data schema
- Valid value enumeration
- Relationship context (star schema)

---

## Testing Prompt Effectiveness

### Test Cases

| Test Query | Expected Operation | Expected Dimensions | Expected Filters |
|------------|-------------------|--------------------|--------------------|
| "Show me Q4 sales by region" | slice | [region] | {quarter: Q4} |
| "Drill into 2024 by quarter" | drill_down | [quarter] | {year: 2024} |
| "Total sales by category" | roll_up | [category] | {} |
| "Compare North and South in Q4" | dice | [region] | {quarter: Q4, region: [North, South]} |
| "What's the trend by month?" | aggregate | [month] | {} |

### Quality Metrics

- **Accuracy**: Correct operation classification
- **Completeness**: All relevant filters extracted
- **Consistency**: Same query produces same output
- **Explainability**: Generated explanation is clear

---

## Future Prompt Enhancements

### 1. Multi-turn Context

```python
# Add conversation history for follow-up queries
system_prompt += f"""
Previous query: {last_query}
Previous result dimensions: {last_dimensions}

User might be asking a follow-up that references the previous analysis.
"""
```

### 2. Ambiguity Resolution

```python
# When uncertain, ask for clarification
"If the query is ambiguous, include a 'clarification_needed' field 
with a question to ask the user."
```

### 3. Suggestion Generation

```python
# Suggest follow-up analyses
"After each analysis, suggest 2-3 relevant follow-up queries the 
user might want to explore."
```

---

## Summary

The prompt design follows these key principles:

1. **Explicit Role Definition** - Clear identity and capabilities
2. **Complete Schema Grounding** - All valid values listed
3. **Structured Output** - Consistent JSON format
4. **Few-Shot Learning** - Examples demonstrating expected behavior
5. **Graceful Defaults** - Sensible fallbacks for ambiguous queries

This approach ensures reliable transformation of natural language to structured OLAP queries while maintaining transparency through the explanation field.
