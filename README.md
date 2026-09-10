
# Hybrid Natural Language SQL Analytics & Visualization Engine

A hybrid natural-language analytics engine that converts user questions into executable SQL, intelligently combining deterministic rule-based processing with LLM-based reasoning for complex analytical queries.

The system uses rule-based SQL generation for straightforward queries and selectively invokes an LLM for complex queries involving CTEs, multi-level aggregation, window functions, ranking, advanced filtering, and other analytical patterns.

Generated SQL is validated before execution, and invalid queries can be automatically repaired using an LLM-based SQL repair workflow. DuckDB is used as the analytical execution engine, while chart generation is handled through deterministic rule-based visualization logic.

## System Architecture

![End-to-End Workflow](https://github.com/BhaskarKosala/Hybrid-Natural-Language-SQL-Analytics-Visualization-Engine/blob/9f623bfb8a14ec30fe455c158e9b89c2217c0721/%20Project%20Flowchart.png)

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
```

### Design Principle

The system deliberately separates deterministic processing from LLM-based reasoning.

Simple queries are handled through predictable rule-based logic, while complex analytical queries are delegated to the LLM. This reduces unnecessary model usage while providing flexibility for queries that require advanced SQL reasoning.

Visualization is also handled independently through deterministic rules, ensuring that chart generation does not depend on LLM output.

## How the Hybrid Query Engine Works

The engine uses a hybrid approach to process natural-language analytical questions.

- **Simple queries** are handled using deterministic rule-based SQL generation.
- **Complex queries** involving CTEs, multi-level aggregation, window functions, ranking, or advanced filtering are routed to an LLM for SQL generation.
- Generated SQL is **validated before execution**.
- If validation fails, the SQL is sent to an **LLM-based repair workflow**.
- Valid SQL is executed using **DuckDB**.
- The resulting data is passed to a **rule-based visualization layer** for chart generation.

This approach combines the reliability and predictability of deterministic logic with the flexibility of LLM reasoning for complex analytical queries.

## Rule-Based Visualization

The engine includes a deterministic visualization layer that converts analytical query results into appropriate charts based on the query type and resulting data structure.

Chart generation is **rule-based and does not require LLM invocation**.

The visualization layer can generate charts for different analytical scenarios, including:

- Categorical comparisons and rankings
- Time-series trends
- Numerical relationships
- Correlation analysis and heatmaps
- Part-to-whole analysis

This creates a complete analytical workflow:

**Natural Language Question → SQL → Data Result → Visualization**

## Screenshots

### Natural Language Query & SQL Generation

![Natural Language Query and Generated SQL](https://github.com/BhaskarKosala/Hybrid-Natural-Language-SQL-Analytics-Visualization-Engine/blob/82997415ff037e2309008139e45baa6a2af46dc6/Simple%20rule-based%20query.png)

### Complex Analytics — AOV Ranking

![Top Customers per State by AOV](https://github.com/BhaskarKosala/Hybrid-Natural-Language-SQL-Analytics-Visualization-Engine/blob/82997415ff037e2309008139e45baa6a2af46dc6/complex%20sql%20and%20ranking.png)

### Rule-Based Visualization — Bar Chart

![Top Customers by Profit](https://github.com/BhaskarKosala/Hybrid-Natural-Language-SQL-Analytics-Visualization-Engine/blob/82997415ff037e2309008139e45baa6a2af46dc6/Rule-based%20analytical%20visualization.png)

### Numerical Analysis — Correlation Heatmap

![Correlation Heatmap](https://github.com/BhaskarKosala/Hybrid-Natural-Language-SQL-Analytics-Visualization-Engine/blob/82997415ff037e2309008139e45baa6a2af46dc6/Correlation%20heatmap.png)

## Technology Stack

- **Programming:** Python
- **Query Language:** SQL
- **Database / Execution Engine:** DuckDB
- **AI / LLM:** LLM-based SQL generation and SQL repair
- **Data Processing:** Pandas
- **Visualization:** Rule-based chart generation
- **Application:** Streamlit

## Future Implementations

- Extend the current hybrid engine to support **arbitrary user-provided datasets**. The existing rule-based query routing and processing are designed to be generic, while the current LLM-based SQL generation is configured around the relationships and schemas of the four sample datasets.
- Make the LLM-based SQL generation **fully dataset-agnostic** by dynamically identifying tables, columns, keys, and relationships from the provided dataset schema instead of relying on predefined relationships.
- Extend visualization capabilities by introducing **LLM-assisted chart generation**, while retaining the existing rule-based visualization approach for deterministic chart generation.
- Expand support for additional analytical query patterns and visualization use cases.
