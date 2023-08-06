import time
import pandas as pd


def hourofday(df: pd.DataFrame, substation_id: str = 'trafo') -> pd.DataFrame:
    """
    This function adds day of week as a feature to the dataframe  and 
    returns just the new feature and substation_id as dataframe

    # Parameters
    --------------
    df: Dataframe with datetime index
    substation_id: refers to column name that keeps substation IDs

    # Returns
    --------------
    Pandas dataframe with substation_id and hourofday features
    
    """

    df_new = df.copy()
    # Create hours of day as a new feature (for example: 0-23)
    df_new['hourofday'] = df_new.index.hour

    return df_new[['hourofday', substation_id]]
