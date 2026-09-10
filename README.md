
# Hybrid Natural Language SQL Analytics & Visualization Engine

A hybrid natural-language analytics engine that converts user questions into executable SQL, intelligently combining deterministic rule-based processing with LLM-based reasoning for complex analytical queries.

The system uses rule-based SQL generation for straightforward queries and selectively invokes an LLM for complex queries involving CTEs, multi-level aggregation, window functions, ranking, advanced filtering, and other analytical patterns.

Generated SQL is validated before execution, and invalid queries can be automatically repaired using an LLM-based SQL repair workflow. DuckDB is used as the analytical execution engine, while chart generation is handled through deterministic rule-based visualization logic.

## Core Pipeline

User Question
      ↓
Intent / Query Detection
      ↓
 ┌───────────────────┐
 │                   │
Simple Query     Complex Query
 │                   │
 ↓                   ↓
Rule-Based       LLM Planner
SQL Generation   + SQL Generation
 │                   │
 │              SQL Validation
 │                   │
 │             ┌─────┴─────┐
 │             │           │
 │            PASS        FAIL
 │             │           │
 │             │       LLM SQL Repair
 │             │           │
 └─────────────┴───────────┘
               ↓
        DuckDB Execution
               ↓
          Data Result
               ↓
    Rule-Based Visualization
               ↓
          Chart / Output

## Key Features

### Hybrid Query Processing
- Uses deterministic rule-based SQL generation for simple analytical queries.
- Selectively routes complex queries to an LLM for advanced SQL generation.
- Avoids unnecessary LLM invocation for straightforward queries.

### Complex SQL Generation
Supports analytical queries involving:
- Common Table Expressions (CTEs)
- Multi-level aggregation
- Window functions
- Ranking
- TOP / BOTTOM-N analysis
- Global and per-group limits
- Threshold-based filtering
- Multiple analytical metrics

### SQL Validation & Repair
- Validates generated SQL before execution.
- Checks SQL structure, schema relationships, aggregation logic, business-metric correctness, and numeric constraints.
- Uses LLM-based SQL repair when generated SQL fails validation.
- Preserves the intent and constraints of the original user question during repair.

### Business Metric Handling
Supports metric-aware SQL generation and validation for:
- Total Sales
- Total Profit
- Total Quantity
- Order Value
- Average Order Value (AOV)

### Rule-Based Visualization
- Automatically determines appropriate visualizations from the query intent and result structure.
- Chart generation is deterministic and does not require LLM invocation.
- Supports analytical visualizations such as bar charts, line charts, and other chart types implemented by the visualization layer.

### Analytical Execution
- Uses DuckDB for SQL execution.
- Converts natural-language analytical questions into executable queries and structured results.

## Architecture

The engine follows a hybrid architecture that combines deterministic logic with LLM reasoning.

```text
                         ┌─────────────────┐
                         │  USER QUESTION  │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │ Intent / Query Detection│
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │ Simple Query │          │Complex Query │
             └──────┬───────┘          └──────┬───────┘
                    │                         │
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │ Rule-Based   │          │ LLM Planner  │
             │ SQL Engine   │          └──────┬───────┘
             └──────┬───────┘                 │
                    │                         ▼
                    │                  ┌──────────────┐
                    │                  │SQL Generation│
                    │                  └──────┬───────┘
                    │                         │
                    │                  ┌──────▼───────┐
                    │                  │SQL Validation│
                    │                  └──────┬───────┘
                    │                         │
                    │                   ┌─────┴─────┐
                    │                   │           │
                    │                  PASS        FAIL
                    │                   │           │
                    │                   │           ▼
                    │                   │     ┌─────────────┐
                    │                   │     │ SQL Repair  │
                    │                   │     │    (LLM)    │
                    │                   │     └──────┬──────┘
                    │                   │            │
                    └───────────────────┴────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │  DuckDB Execution  │
                       └──────────┬─────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Data Result   │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │ Rule-Based Visualization│
                    └────────────┬────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │ Chart / Renderer│
                         └─────────────────┘


### Design Principle

The system deliberately separates deterministic processing from LLM-based reasoning.

Simple queries are handled through predictable rule-based logic, while complex analytical queries are delegated to the LLM. This reduces unnecessary model usage while providing flexibility for queries that require advanced SQL reasoning.

Visualization is also handled independently through deterministic rules, ensuring that chart generation does not depend on LLM output.

