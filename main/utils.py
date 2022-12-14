import pandas as pd

def unname_df_column_remove(original_df):
    df = original_df.loc[:, ~original_df.columns.str.contains('^Unnamed')]
    return df