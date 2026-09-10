import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_datasets
from utils.explorer import display_dataset_explorer
from utils.profiler import display_dataset_profile
from utils.ai_assistant import generate_response
from llm.duckdb_executor import DuckDBExecutor
from utils.ollama_sql import generate_sql
from utils.prompt_builder import build_schema_prompt
from utils.prompt_builder import build_relationship_prompt
from utils.prompt_builder import build_prompt

st.set_page_config(
    page_title="Query Engine",
    layout="wide"
)

# st.title("AI Analytics Studio")
# st.write(
#     "Upload one or more datasets and analyze them using AI"
# )
# st.divider()

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="margin-bottom: 8px;">
            📊 QueryEngine
        </h1>
        <p style="font-size: 18px; color: #9ca3af;">
            Rule-Based & LLM-Powered Data Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()
st.subheader("📂 Upload Datasets")

uploaded_files = st.file_uploader(
    "Choose CSV or Excel files",
    type=["csv","xlsx"],
    accept_multiple_files=True
)

if "datasets" not in st.session_state:
    st.session_state.datasets = {}

if uploaded_files:
    st.session_state.datasets = load_datasets(
        uploaded_files
    )
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

    # from utils.helpers import find_dataset
    # print(find_dataset("average age", st.session_state.datasets))
    # print(find_dataset("maximum price", st.session_state.datasets))
    # print(find_dataset("count payment_method", st.session_state.datasets))

    # from utils.helpers import find_relationship
    # print(find_relationship("customers","orders"))
    # print(find_relationship("orders","customers"))
    # print(find_relationship("products","order_items"))

    # from utils.helpers import find_all_relationships
    # from utils.join_helper import join_multiple_datasets
    # relationships = find_all_relationships(st.session_state.datasets)
    # result = join_multiple_datasets(
    #     ["customers", "orders", "order_items"],
    #     st.session_state.datasets,
    #     relationships
    # )
    # print(result.head())

    st.divider()
    st.subheader("📊 Datasets Overview")
    display_dataset_profile(
        st.session_state.datasets
    )

    #st.divider()
    display_dataset_explorer(
        st.session_state.datasets
    )

    # schema = build_schema_prompt(
    #     st.session_state.datasets
    # )
    # print(schema)

    # print(build_relationship_prompt())

    # prompt = build_prompt(
    #     "Top 5 product categories by profit",
    #     st.session_state.datasets
    # )
    # ollama_response = generate_sql(prompt)
    # print(ollama_response)

    # executor = DuckDBExecutor()
    # executor.register_datasets(
    #     st.session_state.datasets
    # )
    # result = executor.execute("""
    # SELECT
    #     customers.customer_name,
    #     order_items.profit
    # FROM customers
    # JOIN orders
    #     ON customers.customer_id = orders.customer_id
    # JOIN order_items
    #     ON orders.order_id = order_items.order_id
    # ORDER BY order_items.profit DESC
    # LIMIT 10;
    # """)
    # print(result)

    st.divider()
    st.subheader("🤖 AI Assistant")
    question = st.text_input(
        "Ask anything about your datasets..."
    )
    if question:
        response = generate_response(
            question,
            st.session_state.datasets
        )
        print("UI response:", response)

        # executor = DuckDBExecutor()
        # executor.register_datasets(
        #     st.session_state.datasets
        # )
        #print("UI response:", response)

        if isinstance(response, dict):
            if "sql" in response:
                with st.expander("⛁ Generated SQL", expanded=False):
                    st.code(
                        response["sql"],
                        language="sql"
                    )
            if response["type"] == "dataset_list":
                st.subheader("📂 Loaded Datasets")
                st.write(f"There are **{response['count']}** dataset(s):")
                for dataset in response["datasets"]:
                    st.write(f"• {dataset}")
            elif response["type"] == "row_count":
                st.subheader("📊 Dataset Information")
                st.write(
                    f"**{response['dataset']}** contains "
                    f"**{response['rows']}** rows."
                )
            elif response["type"] == "schema":
                st.subheader("🗂️ Dataset Schema")
                st.write(
                    f"📄 **{response['dataset']}** Schema"
                )
                schema_df = pd.DataFrame({
                    "Column": response["dataframe"].columns,
                    "Data Type":
                        response["dataframe"]
                        .dtypes
                        .astype(str)
                        .values
                })
                st.dataframe(
                    schema_df,
                    use_container_width=True,
                    hide_index=True
                )
            elif response["type"] == "summary":
                st.subheader("📊 Dataset Summary")
                st.caption(f"📄 {response['dataset']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rows", response["rows"])
                    st.metric("Columns", response["columns"])
                    st.metric(
                        "Numeric Columns",
                        response["numeric_columns"]
                    )
                    st.metric(
                        "Categorical Columns",
                        response["categorical_columns"]
                    )
                with col2:
                    st.metric(
                        "Datetime Columns",
                        response["datetime_columns"]
                    )
                    st.metric(
                        "Missing Values",
                        response["missing_values"]
                    )
                    st.metric(
                        "Duplicate Rows",
                        response["duplicate_rows"]
                    )
                    st.metric(
                        "Memory (KB)",
                        response["memory_usage"]
                    )
            elif response["type"] == "dataset_contents":
                st.subheader(f"📄 {response['dataset']}")
                st.caption(
                    f"{len(response['dataframe'])} rows x "
                    f"{len(response['dataframe'].columns)} columns"
                )
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True
                )
            elif response["type"] == "statistics":
                st.subheader("📊 Column Statistics")
                st.caption(
                    f"📄 {response['dataset']} • 🔢 {response['column']}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Count", response["count"])
                    st.metric("Mean", response["mean"])
                    st.metric("Median", response["median"])
                with col2:
                    st.metric("Std Dev", response["std"])
                    st.metric("Minimum", response["min"])
                    st.metric("Maximum", response["max"])
            elif response["type"] == "unique_values":
                st.subheader("📋 Unique Values")
                st.caption(
                    f"📄 **{response['dataset']}** • 🏷️ **{response['column']}**"
                )
                st.metric(
                    "Distinct Values",
                    response["count"]
                )
                unique_df = pd.DataFrame(
                    {"Distinct Values": response["values"]}
                )
                st.dataframe(
                    unique_df,
                    hide_index=True,
                    use_container_width=True
                )
            elif response["type"] == "value_counts":
                st.subheader("📊 Value Counts")
                st.caption(
                    f"📄 {response['dataset']} • 🏷️ {response['column']}"
                )

                st.dataframe(
                    response["dataframe"],
                    hide_index=True,
                    use_container_width=True
                )
            elif response["type"] == "top_values":
                st.subheader(f"📈 Top {response['top_n']} Values")
                st.caption(
                    f"📄 {response['dataset']} • 🏷️ {response['column']}"
                )
                st.dataframe(
                    response["dataframe"],
                    hide_index=True,
                    use_container_width=True
                )
            elif response["type"] == "bottom_values":
                st.subheader(f"📉 Bottom 5 Values")
                st.write(
                    f"📄 {response['dataset']} • 🏷️ {response['column']}"
                )
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True,
                    hide_index=True
                )
            elif response["type"] == "missing_values":
                st.subheader("📋 Missing Values")
                st.write(
                    f"📄 {response['dataset']}"
                )
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True,
                    hide_index=True
                )
            elif response["type"] == "no_missing_values":
                st.success(
                    f"✅ No Missing Values found in {response['dataset']}"
                )
            elif response["type"] == "filtered_data":
                st.subheader("🔍 Filter Results")
                st.write(
                    f"📄 {response['dataset']} • {response['column']} = {response['value']}"
                )
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True,
                    hide_index=True
                )
            elif response["type"] == "aggregation":
                st.subheader("📊 Aggregation Result")
                st.write(
                    f"📄 {response['dataset']} • 🔢 {response['column']}"
                )
                st.metric(
                    label=response['metric'],
                    value=response['value']
                )
            elif response["type"] == "groupby":
                st.subheader("📊 Group By Result")
                st.caption(
                    f"📄 {response['dataset']}"
                )
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True
                )
            elif response["type"] == "sort":
                st.subheader("📋 Sorted Result")
                st.caption(response["dataset"])
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True
                )
            elif response["type"] == "topbottom":
                st.subheader("🏆 Top/Bottom Result")
                st.caption(response["dataset"])
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True
                )
            elif response["type"] == "filter":
                st.subheader("🔍 Filtered Result")
                st.caption(response["dataset"])
                st.dataframe(
                    response["dataframe"],
                    use_container_width=True,
                    hide_index=True
                )
            elif response["type"] == "chart":
                st.subheader(response["dataset"])
                original_df = response["dataframe"]
                chart_df = original_df.set_index(
                    original_df.columns[0]
                )
                chart_type = response["chart_type"]
                #print("Chart Type:", chart_type)
                #print(chart_df)
                if chart_type == "bar":
                    st.bar_chart(chart_df)
                elif chart_type == "line":
                    st.line_chart(chart_df)
                elif chart_type == "area":
                    st.area_chart(chart_df)
                elif chart_type == "horizontal_bar":
                    st.bar_chart(
                        chart_df,
                        horizontal=True
                    )
                
                elif chart_type == "pie":
                    value_columns = response.get("value_columns", [])
                    if len(value_columns) > 1:
                        value_column = value_columns[0]
                    else:
                        value_column = value_columns[0]

                    fig, ax = plt.subplots()
                    ax.pie(
                        original_df[value_column],
                        labels=original_df.iloc[:, 0],
                        autopct="%1.1f%%"
                    )
                    ax.set_title(f"{value_column.title()} Distribution")
                    st.pyplot(fig)
                    # ax.pie(
                    #     original_df.iloc[:,1],
                    #     labels=original_df.iloc[:,0],
                    #     autopct="%1.1f%%"
                    # )
                    # ax.set_title("Pie Chart")
                    # st.pyplot(fig)
                elif chart_type == "scatter":
                    #numeric_df = original_df.select_dtypes(include="number")
                    x_column = response["x_column"]
                    y_columns = response["y_columns"]
                    if not y_columns:
                        st.warning(
                            "Scatter plot requires two numeric columns."
                        )
                    else:
                        fig, ax = plt.subplots()
                        ax.scatter(
                            original_df[x_column],
                            original_df[y_columns[0]]
                        )
                        ax.set_xlabel(x_column)
                        ax.set_ylabel(y_columns[0])
                        st.pyplot(fig)

                elif chart_type == "histogram":
                    value_column = response["value_column"]
                    fig, ax = plt.subplots()
                    ax.hist(original_df[value_column], bins=20)
                    ax.set_xlabel(value_column)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)
                elif chart_type == "box":
                    value_column = response["value_column"]
                    fig, ax = plt.subplots()
                    ax.boxplot(
                        original_df[value_column].dropna(),
                        patch_artist=True,
                        showmeans=True
                    )
                    ax.set_ylabel(value_column)
                    ax.grid(axis="y", linestyle="--", alpha=0.5)
                    ax.set_title(f"Box Plot of {value_column}")
                    st.pyplot(fig)
                elif chart_type == "heatmap":
                    correlation_df = original_df
                    fig, ax = plt.subplots(figsize=(8,6))
                    im = ax.imshow(correlation_df, cmap="coolwarm", vmin=-1, vmax=1)
                    ax.set_xticks(range(len(correlation_df.columns)))
                    ax.set_yticks(range(len(correlation_df.index)))
                    ax.set_xticklabels(
                        correlation_df.columns,
                        rotation=45,
                        ha="right"
                    )
                    ax.set_yticklabels(correlation_df.index)
                    for i in range(len(correlation_df.index)):
                        for j in range(len(correlation_df.columns)):
                            ax.text(
                                j,
                                i,
                                f"{correlation_df.iloc[i,j]:.2f}",
                                ha="center",
                                va="center",
                                fontsize=9
                            )
                    plt.colorbar(im)
                    ax.set_title("Correlation Heatmap")
                    st.pyplot(fig)
                st.dataframe(
                    response["dataframe"],
                    hide_index=True,
                    use_container_width=True
                )
            elif response["type"] == "text":
                st.error(response["message"])
            elif response["type"] == "table":
                st.subheader(f"📊 {response['dataset']}")
                #print("Displaying Dataframe:")
                #print(response["dataframe"])
                st.dataframe(
                    response["dataframe"],
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.markdown(response)