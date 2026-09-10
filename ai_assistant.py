import pandas as pd
import os
from utils.handlers.profile import handle__profile
from utils.handlers.profile import handle_dataset_info
from utils.handlers.profile import handle_missing_values
from utils.handlers.profile import handle_dataset_contents
from utils.handlers.statistics import handle_statistics
from utils.handlers.statistics import handle_unique_values
from utils.handlers.statistics import handle_value_counts
from utils.handlers.aggregation import handle_aggregation
from utils.handlers.sort import handle_sort
from utils.handlers.where import handle_where
from utils.handlers.groupby import handle_simple_groupby
from utils.handlers.groupby import handle_groupby_aggregation
from utils.handlers.top_bottom import handle_top_bottom
from utils.helpers import find_dataset
from utils.handlers.join import handle_join
from utils.chart_helper import wants_chart
# from utils.handlers.charts import(
#     handle_heatmap,
#     handle_scatter,
#     handle_histogram,
#     handle_boxplot
# )
from utils.chart_helper import get_chart_type
from utils.helpers import get_best_dataset_for_heatmap
from utils.intent import detect_intent
from utils.handlers.charts import handle_chart
from utils.join_helper import get_joined_dataframe
from utils.handlers.llm_response import generate_llm_response
#from utils.handlers.order_value import handle_order_value
#from utils.helpers import get_display_column
#from utils.helpers import extract_sort
# from utils.helpers import (
#     apply_sort,
#     apply_limit
# )

def generate_response(question,datasets):
    #print("Question Recieved :", repr(question))
    question = question.lower().strip()
    if wants_chart(question):
        intent = "chart"
    else:
        intent = detect_intent(question, datasets)
    print("Final Intent:", intent)

    # if intent == "order-value":
    #     response = handle_order_value(question, datasets)
    #     if response:
    #         return response
    #print("Sort:", extract_sort(question))
    if intent == "join" and not wants_chart(question):
        response = handle_join(question, datasets)
        if response:
            return response
    print("Question:", question)
    print("Intent:", intent)

    if intent == "dataset_info":
        response = handle_dataset_info(question, datasets)
        if response:
            return response

    selected_dataset = find_dataset(question, datasets)
    df = None
    if (
        isinstance(selected_dataset, list)
    ):
        if intent in [
            "where",
            "sort",
            "top-bottom",
            "groupby",
            "aggregation"
        ]:
            selected_dataset = selected_dataset[0]
        elif intent != "chart":

            return(
                "Please specify the dataset. The column exists in: "
                + ", ".join(selected_dataset)
            )
    elif selected_dataset is None:
        if get_chart_type(question) == "heatmap":
            selected_dataset = get_best_dataset_for_heatmap(datasets)
        elif wants_chart(question) and len(datasets) == 1:
            selected_dataset = next(iter(datasets))
        else:
            return (
                "Please specify the dataset.\n\n"
                + "\n".join(datasets.keys())
            )
    
    if isinstance(selected_dataset, str):

        df = datasets[selected_dataset]
        # print(
        #     "Display Column:",
        #     get_display_column(df)
        # )

    # if intent == "analysis":
    #     result = df.copy()
    #     result = apply_sort(result, question)
    #     result = apply_limit(result, question, value_columns)

    if intent == "chart":
        print("wants_chart:", wants_chart(question))
        print("Intent:", intent)
        mentioned, chart_df = get_joined_dataframe(
            question,
            datasets
        )
        if chart_df is None:
            chart_df = df
        if mentioned is None:
            mentioned = [selected_dataset]
            
        response = handle_chart(
            question,
            " + ".join(mentioned),
            chart_df
        )
        #response = handle_chart(question, selected_dataset, df)
        if response:
            return response  
    elif intent == "profile":
        response = handle__profile(question, selected_dataset, df)
        if response:
            return response
        
        response = handle_missing_values(question, selected_dataset, df)
        if response:
            return response
        
        response = handle_dataset_contents(question, selected_dataset, df)
        if response:
            return response
    
    elif intent == "statistics":
        print("Entered statistics block")
        response = handle_statistics(question, selected_dataset, df, datasets)
        if response:
            return response
        
        response = handle_unique_values(question, selected_dataset, df, datasets)
        if response:
            return response
        
        response = handle_value_counts(question, selected_dataset, df, datasets)
        if response:
            return response
    
    elif intent == "aggregation":
        complex_aggregation = any(
            phrase in question.lower()
            for phrase in [
                "order value",
                "average order",
                "maximum order",
                "minimum order",
                "total order",
                "more than",
                "less that",
                "at least",
                "fewer than",
                "customers with",
                "customers who"
            ]
        )
        if complex_aggregation:
            return generate_llm_response(
                question,
                datasets
            )

        response = handle_aggregation(question, selected_dataset, df, datasets)
        if response:
            return response
       
    elif intent == "where":
        response = handle_where(question, selected_dataset, df, datasets)
        if response:
            return response
    
    elif intent == "groupby":
        # response = handle_simple_groupby(question, selected_dataset, df, datasets)
        # if response:
        #     return response
        
        # response = handle_groupby_aggregation(question, selected_dataset, df, datasets)
        # if response:
        #     return response

        return generate_llm_response(
            question,
            datasets
        )
    
    elif intent == "top-bottom":
        response = handle_top_bottom(question, selected_dataset, df, datasets)
        if response:
            return response
        
    elif intent == "sort":
        response = handle_sort(question, selected_dataset, df, datasets)
        if response:
            return response
        
 

    return generate_llm_response(
        question,
        datasets
    )