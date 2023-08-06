import pandas as pd
from datetime import timedelta
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
