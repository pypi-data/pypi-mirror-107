import time
import pandas as pd


def shifted_hourly_load(df: pd.DataFrame,
                        t: int = 72,
                        cols: str = 'aggregated_per_mp',
                        sort: str = 'trafo') -> pd.DataFrame:
    '''
    Adds a feature to the dataframe containing the T-t previous data where T is current time. 
    Then return dataframe with shifted feature and substation_ID columns.
    For example t=1 adds data from 1 hour back. 

    # Parameters
    --------------
    df: dataframe
    t: Shifting hour
    cols: The column where shifting is based on
    sort: refers to column name that keeps substation IDs

    # Returns
    --------------
    Dataframe with shifted time feature and substation_ID columns

    '''
    df_new = df.copy()

    feature_name = 'd_' + str(t)
    # dff = df_new.groupby(sort)[cols].shift(periods=t, freq = 'H').to_frame()
    # dff.rename(columns={"aggregated_per_mp": feature_name}, inplace = True)
    # dff.reset_index(inplace=True)
    # dff = dff.set_index('date_tz')

    # print("dff is printing", dff.head())
    # print("dff is printing", dff.tail())

    df_new[feature_name] = df_new.groupby(sort)[cols].shift(periods=t)
    # print("dataframe yazdiriliyor", df_new[[feature_name, sort]].head())
    return df_new[[feature_name, sort]]

    # return dff
