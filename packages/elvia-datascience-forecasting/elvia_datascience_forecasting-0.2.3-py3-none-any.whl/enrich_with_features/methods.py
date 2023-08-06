import pandas as pd
import pandas as pd
from azureml.core import Dataset
from datetime import timedelta
from datetime import timedelta, datetime
from .features.add_metadata import add_metadata
from .features.dayofweek import dayofweek
from .features.hourofday import hourofday
from .features.monthyear import monthyear
from .features.hourofweek import hourofweek
from .features.school_holiday import school_holiday
from .features.national_holiday import national_holiday
from .features.temperature_hourly import temperature_hourly
from .features.average_weekly_data import average_weekly_data
from .features.shifted_hourly_load import shifted_hourly_load
from .features.sin_cos_cyclical_feature import sin_cos_transformation


def enrich(df: pd.DataFrame,
           df_weekly,
           holiday_path: str = '',
           token_weather: str = '',
           time_zone: bool = False,
           deployment: bool = False) -> pd.DataFrame:
    """
    This function takes in substations load as dataframe(df) and adds new features to 
    the dataframe which will be used to build machine learning models

    # Parameters
    --------------
    df          : Dataframe of consumption data'
    df_weekly   : Weekly average cumsumtion AZURE DATASET
    holiday_path: The path of the json file that contains dates of national and school holidays
    token_weather: Token for Weather API
    time_zone   : Weather data comes with timezone UTC. It can be set to Oslo-timezone by writing 'time_zone = True'
    deployment  : If this function is used in deployment step, it should be set as 'True'

    # Returns
    --------------
    A pandas dataframe without index of 'date_tz' and feature of 'trafo'
    """

    df = df.set_index('date_tz')

    # Adding 72, 96 and 168 hours shifting
    for hour in [72, 96, 168]:
        df_shift = shifted_hourly_load(df, t=hour)
        # Merging dataframes by index date_tz and substation_ID column
        df = df.merge(df_shift,
                      left_on=['date_tz', 'trafo'],
                      right_on=['date_tz', 'trafo'],
                      how='left')

    # Adding days of a week to dataframe
    df_day = dayofweek(df)
    df = df.merge(df_day,
                  left_on=['date_tz', 'trafo'],
                  right_on=['date_tz', 'trafo'],
                  how='left')

    # Adding hours of a day to dataframe
    df_hour = hourofday(df)
    df = df.merge(df_hour,
                  left_on=['date_tz', 'trafo'],
                  right_on=['date_tz', 'trafo'],
                  how='left')

    # Adding hour of week to dataframe (0 - 167)
    df_weekhour = hourofweek(df)
    df = df.merge(df_weekhour,
                  left_on=['date_tz', 'trafo'],
                  right_on=['date_tz', 'trafo'],
                  how='left')

    # Adding month of a year to dataframe
    df_month = monthyear(df)
    df = df.merge(df_month,
                  left_on=['date_tz', 'trafo'],
                  right_on=['date_tz', 'trafo'],
                  how='left')

    df.reset_index(
        inplace=True
    )  # we reset index before merging with average_weekly_data, otherwise we will lose 'date_tz' index
    # Adding month of a year to dataframe
    df_average_weekly = average_weekly_data(df_weekly)
    df = df.merge(df_average_weekly,
                  left_on=['hourofweek', 'trafo'],
                  right_on=['houroftheweek', 'trafo'],
                  how='left')
    df = df.set_index('date_tz')  # setting index again

    # Adding school holiday to dataframe
    df_school_holiday = school_holiday(df, path_holiday=holiday_path)
    df = df.merge(df_school_holiday,
                  left_on=['date_tz', 'trafo'],
                  right_on=['date_tz', 'trafo'],
                  how='left')
    df['school_holiday'] = df['school_holiday'].astype(
        'bool')  # casting type from object to boolean

    # Adding national holiday to dataframe
    df_national_holiday = national_holiday(df, path_holiday=holiday_path)
    df = df.merge(df_national_holiday,
                  left_on=['date_tz'],
                  right_on=['date_tz'],
                  how='left')

    # Adding Weather data
    start_date = df.index[0].strftime(format='%Y-%m-%d')
    end_date = (df.index[-1] + timedelta(days=1)).strftime(format='%Y-%m-%d')
    df_weather = temperature_hourly(df,
                                    'temperature',
                                    start_date=start_date,
                                    end_date=end_date,
                                    time_zone=time_zone,
                                    weather_token_id=token_weather)
    # Reset index to merge dataframes based on index column and trafo column
    df.reset_index(drop=False, inplace=True)
    df = df.merge(df_weather,
                  left_on=['date_tz', 'trafo'],
                  right_on=['time', 'trafo'],
                  how='left')

    # Drop these columns because we will not use them in ML model
    df.drop('time', axis=1, inplace=True)

    # Sine and cosine transformation
    cyclical_features = [('hourofday', 23), ('dayofweek', 6),
                         ('monthyear', 12)]
    for col in cyclical_features:
        sin_cos_transformation(df, col[0], col[1])

    if deployment:
        # Drop the 3 cyclical features and other columns because we will not use them in ML model
        df.drop([
            'aggregated_per_mp', 'trafo', 'date_tz', 'hourofday', 'dayofweek',
            'monthyear', 'hourofweek', 'houroftheweek', 'station_name',
            'kommunenavn', 'kommunenummer', 'fylkesnavn', 'fylkesnummer',
            'Driftsmerking', 'long', 'lat'
        ],
                axis=1,
                inplace=True)
    else:
        # Drop the 3 cyclical features and other columns because we will not use them in ML model
        df.drop([
            'hourofday', 'dayofweek', 'monthyear', 'hourofweek',
            'houroftheweek', 'station_name', 'kommunenavn', 'kommunenummer',
            'fylkesnavn', 'fylkesnummer', 'Driftsmerking', 'long', 'lat'
        ],
                axis=1,
                inplace=True)

    return df


def ingest_data(azure_dataset: Dataset,
                df_metadata: pd.DataFrame,
                last_day: datetime = None,
                first_day: datetime = None,
                percentage: int = 0.9,
                trafo_name: str = '',
                deployment: bool = False,
                time_zone: bool = False) -> pd.DataFrame:
    '''
    This function takes in Azure energy consumption dataset and its Azure metadata dataset. Substation Ids in the Azure energy consumption dataset
    will be renamed by using Driftsmerking name in the Azure metadata dataset. 

    # Parameters
    --------------
    azure_dataset : Azure energy consumption dataset
    df_metadata   : Energy consumption Azure metadata dataset
    last_day      : Last day of the energy consumption data (datetime(year, month, day, hour, minute, second) )
    first_day     : First day of the energy consumption data (datetime(year, month, day, hour, minute, second) )
    percentage    : Percentage that is used to select the appropriate transformers
    time_zone     : Substation data comes with timezone UTC. It can be set to Oslo-timezone by writing 'time_zone = True'
    deployment    : If this function is used in deployment, it should be set as 'True', otherwise 'False'

    # Returns
    --------------
    A pandas dataframe with the transformers that has rows greater than determined percentage(90%) of the number of hours in the selected date range
    '''
    df = azure_dataset.to_pandas_dataframe()

    df = df.rename(columns={"dtm": "date_tz"})  # change series name
    df['date_tz'] = pd.to_datetime(
        df['date_tz'], infer_datetime_format=True,
        utc=True)  # convert object date to datetime64[ns, UTC]
    df.sort_values(by=['trafo', 'date_tz'], inplace=True)

    if deployment:
        df = df.loc[df['trafo'] == trafo_name]

        # Adding 67 hours to the index
        df = df.set_index('date_tz')
        other = pd.DataFrame([],
                             columns=df.columns,
                             index=[df.shift(freq='67H').index[-67:]])
        other.reset_index(inplace=True)
        df.reset_index(inplace=True)
        df = df.append(other)
        # filling NaN values. ‘ffill’ stands for ‘forward fill’ and will propagate last valid observation forward.
        df = df.ffill()

        # Filtering last 10 days of the dataset because it is just needed last 7 days for predicting 67 hours ahead
        df = df.set_index('date_tz')
        end_date = (df.index[-1] +
                    timedelta(days=-10)).strftime(format='%Y-%m-%d')
        df.reset_index(inplace=True)
        df = df.loc[df['date_tz'] >= end_date]

    else:
        # Selects transformers with rows greater than 90% of the number of hours in the selected date range
        date_range = last_day - first_day
        diff_hour = date_range.total_seconds(
        ) / 3600  # difference based on hour

        X_columns_list = list(df.columns.values.tolist())
        df_ranged = pd.DataFrame(columns=X_columns_list)
        for station_id in df['trafo'].unique():
            data_set = df.loc[df.trafo == station_id]
            if len(data_set) < diff_hour * percentage:
                continue
            df_ranged = df_ranged.append(data_set, ignore_index=True)
        df = df_ranged

    df.sort_values(by=['trafo', 'date_tz'], inplace=True)
    # Merging dataframe with substation metadata to add kommunenavn, latitude and longitude to the dataframe
    df['station_name'] = df.trafo.apply(add_metadata, df_metadata=df_metadata)
    df = df.merge(df_metadata,
                  left_on=['station_name'],
                  right_on=['Driftsmerking'],
                  how='left')

    if time_zone == True:
        df = df.set_index('date_tz')
        # Convert to 'Europe/Oslo' time zone
        df.index = df.index.tz_convert(tz='Europe/Oslo')
        df.reset_index(inplace=True)

    return df
