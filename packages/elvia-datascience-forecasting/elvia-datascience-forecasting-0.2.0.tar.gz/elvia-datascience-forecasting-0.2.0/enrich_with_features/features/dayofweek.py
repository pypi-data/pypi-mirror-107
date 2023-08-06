import time
import pandas as pd


def dayofweek(df: pd.DataFrame, substation_id: str = 'trafo') -> pd.DataFrame:
    """
    This function adds day of week as a feature to the dataframe  and 
    returns just the new feature and substation_id as dataframe

    # Parameters
    --------------
    df: Dataframe with datetime index
    substation_id: refers to column name that keeps substation IDs

    # Returns
    --------------
    Pandas dataframe with substation_id and dayofweek features
    
    """
    df_new = df.copy()
    dict = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}

    # Create day of week as a new feature (for example: 0-sunday, 6-saturday)
    df_new["dayofweek"] = df_new.index.dayofweek
    df_new["dayofweek"] = df_new["dayofweek"].map(dict)

    return df_new[["dayofweek", substation_id]]
