import time
import pandas as pd


def hourofweek(df: pd.DataFrame, substation_id: str = 'trafo') -> pd.DataFrame:
    """
    This function adds day of week as a feature to the dataframe  and 
    returns just the new feature and substation_id as dataframe

    # Parameters
    --------------
    df: Dataframe with datetime index
    substation_id: refers to column name that keeps substation IDs

    # Returns
    --------------
    Pandas dataframe with substation_id and hourofweek features
    
    """

    df_new = df.copy()
    # Create day of week as a new feature (for example: 0-monday, 6-sunday)
    df_new["hourofweek"] = df_new["dayofweek"] * 24 + df_new['hourofday']

    return df_new[["hourofweek", substation_id]]
