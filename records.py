import pandas as pd
import logic

def record_kid(code_kid, current_gala, record_col, output_df:pd.DataFrame, input_df:pd.DataFrame):
    index_kid = logic.find_index_kid(code_kid, input_df)

