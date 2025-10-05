import pandas as pd 
import numpy as np 
from datetime import datetime as dt
from .outlier_detection import remove_outliers

def pace_zone(pace: float) -> str:
    '''Takes a pace(float) as an input and return a pace zone(str).'''
    paces = {
        "very_fast (p< 4:00)": lambda p: p < 4,
        "fast (p< 4:30)": lambda p: p < 4.30,
        "moderate (p< 5:00)": lambda p: p < 5,
        "easy (p< 6:00)": lambda p: p < 6,
        "recovery (p> 6)": lambda p: p >= 6
    }

    for zone, condition in paces.items():
        if condition(pace):
            return zone

    return "unknown"



# Function to convert avg pace minutes to min:sec
def avg_pace_to_min_sec(decimal_minutes):
    """
    Convert decimal minutes to min:sec format.
    
    Parameters:
        decimal_minutes (float): Time in decimal minutes, e.g., 4.153
    
    Returns:
        str: Formatted string in min:sec, e.g., "4:09"
    """
    minutes = int(decimal_minutes)                # Get whole minutes
    seconds = round((decimal_minutes - minutes) * 60)  # Convert decimal part to seconds
    return f"{minutes}:{seconds:02d}"             # Format with leading zero if needed


def clean_data(df):
    #Changing the capital format into the lower format replacing the space in between features names by _
    df.columns= df.columns.str.lower().str.replace(" ", "_")
    
    # The useful columns.
   
    useful_columns =['activity_id',
    'activity_date',
    'elapsed_time',
    'distance',
    'moving_time',
    'average_speed',
    'elevation_gain',
    'elevation_loss',
    'average_grade',
    'grade_adjusted_distance',
    'dirt_distance',
    'average_grade_adjusted_pace']
    
    # Using only the useful columns since others contains either NaN values or are useless. 
    df1= df[useful_columns].copy()
    
    # Creating extra columns to create numerics which aren't in the dataset already
    df1['elapsed_minute'] = df1['elapsed_time'] / 60
    df1['moving_mins'] = df1['moving_time'] / 60
    df1["km_per_hour"] = df1['distance']/ (df1['moving_mins']/60)
    df1['avg_pace'] = df1['moving_mins']/ df1['distance']
    df1['pace_min_sec'] = df1['avg_pace'].apply(avg_pace_to_min_sec)
    df1['pace_zone'] = df1['avg_pace'].apply(pace_zone)
    df1['average_grade_adjusted_pace'] = df1['average_grade_adjusted_pace'].fillna(df1['average_grade_adjusted_pace'].mean())
    # We use the datetime module to convert the activity_date column to a datetime format. 

    df1["activity_date"] = pd.to_datetime(df1['activity_date'])
    df1["start_time"] = df1["activity_date"].dt.time 
    df1["start_date_local"] = df1["activity_date"].dt.date
    df1["month"] = df1["activity_date"].dt.month_name()
    df1['year'] = df1["activity_date"].dt.year
    df1['year'] = df1['year'].astype(object) #change year from numeric to object
    df1['dayofyear'] = df1["activity_date"].dt.dayofyear
    df1['dayofyear'] = pd.to_numeric(df1['dayofyear'])
   
    
    cleanest_data = remove_outliers(df1)
    return df1, cleanest_data