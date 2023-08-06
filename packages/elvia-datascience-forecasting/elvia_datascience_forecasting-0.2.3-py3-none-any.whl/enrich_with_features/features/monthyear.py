import time
import pandas as pd


def monthyear(df: pd.DataFrame, substation_id: str = 'trafo') -> pd.DataFrame:
    """
     This function adds day of week as a feature to the dataframe  and 
     returns just the new feature and substation_id as dataframe

     # Parameters
     --------------
     df: Dataframe with datetime index
     substation_id: refers to column name that keeps substation IDs

     # Returns
     --------------
     Pandas dataframe with substation_id and monthyear features
    
     """

    df_new = df.copy()
    # Create months of of a year as a new feature (for example: 1-Januar, 12-December)
    df_new['monthyear'] = df_new.index.month

    return df_new[['monthyear', substation_id]]
