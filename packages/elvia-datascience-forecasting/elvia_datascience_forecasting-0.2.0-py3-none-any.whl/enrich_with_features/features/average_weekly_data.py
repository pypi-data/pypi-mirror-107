import pandas as pd


def average_weekly_data(tab_data_set):
    """
    This function takes into Azure dataset of the average weekly data  and 
    returns a pandas dataframe

    tab_data_set: Azure tabular dataset
    """

    return tab_data_set.to_pandas_dataframe()
