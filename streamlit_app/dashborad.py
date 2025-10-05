import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plost 
import altair as alt
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.cleaning_data import clean_data

def format_time(minutes):
    """
    Convert a time in minutes to a human-readable format.
    
    - If less than 60 minutes → return "XX mins"
    - If 60 minutes or more → return "HH:MM hrs"
    
    Args:
        minutes (float or int): Time in minutes.
        
    Returns:
        str: Formatted time string.
    """
    if minutes < 60:
        return f"{float(minutes)} mins"
    else:
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}:{mins:02d} hrs"  # ensures 2 digits for minutes

# Build KPI ( Key Performance Indicators )

def dash_bord(data_file, time_frame: str=None):
    st.subheader('📊Dashboards')
    
    st.set_page_config(layout="wide")
    # css_path = Path(__file__).resolve().parent / "style.css"
    # with open(css_path) as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # creating a session state variable for the dataframe
    if not data_file:
        if "data_outliers" not in st.session_state:
            st.session_state.data_outliers = None 
        # st.info('Awaiting for CSV file to be uploaded.')
    else:
        st.session_state.data_outliers = pd.read_csv(data_file)
        # st.write(st.session_state.dataframe)
    
        data_outliers, data_no_outliers = clean_data(df=st.session_state.data_outliers)
        
        total_distance = round(float(data_outliers['distance'].sum()),2)
        total_distance = f"{total_distance} km"
        
        total_runs = data_outliers.shape[0]
        total_runs = f"{total_runs} runs"
        
        total_time = float(round(data_outliers['moving_mins'].sum(),2))
        total_time= f"{format_time(total_time)} secs"
        
        # obtainig the average pace
        avg_pace = float(round(data_outliers['avg_pace'].mean(),2))
        avg_pace = f"{avg_pace} mins/km"
        
        #best performance in the 5km. 
        
        frame_5k = data_outliers[(data_outliers['distance'] >= 5) & (data_outliers['distance'] <= 5.05)]
        time_5k = round(frame_5k['moving_mins'].min(),2)
        time_5k = format_time(time_5k)
        pace_5k = frame_5k[frame_5k['moving_mins'] == frame_5k['moving_mins'].min()]
        pace_5k = pace_5k['pace_min_sec'].iloc[0]
        
        #best performance in the 10km. 
        
        frame_10k = data_outliers[(data_outliers['distance'] >= 10) & (data_outliers['distance'] <= 10.10)]
        time_10k = round(frame_10k['moving_mins'].min(),2)
        time_10k = format_time(time_10k)
        pace_10k = frame_10k[frame_10k['moving_mins'] == frame_10k['moving_mins'].min()]
        pace_10k = pace_10k['pace_min_sec'].iloc[0]
        
        #best performance in the 10km. 
        
        frame_21k = data_outliers[(data_outliers['distance'] >= 21) & (data_outliers['distance'] <= 21.11)]
        time_21k = round(frame_21k['moving_mins'].min(),2)
        time_21k = format_time(time_21k)
        pace_21k = frame_21k[frame_21k['moving_mins'] == frame_21k['moving_mins'].min()]
        pace_21k = pace_21k['pace_min_sec'].iloc[0]

        
        # Build KPI ( Key Performance Indicators )
        st.markdown('**🏃 1. Key Running Stat (KPI)**')
        
        # Row A 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.markdown(" **🏃 Total Distance**")
                st.markdown(f"{total_distance}")
        with col2:
            with st.container(border=True):
                st.markdown(' **🏃 Total Run**')
                st.markdown(f"{total_runs}")
        with col3:
            with st.container(border=True):
                st.markdown(" **⏱️ Total Duration**")
                st.markdown(f"{total_time}")
        with col4:
            with st.container(border=True):
                st.markdown(" **🏃 avg_pace**")
                st.markdown(f"{avg_pace}")
            
        # Row B ⏱️
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container(border=True):
                st.markdown('**🏃 5km best effort**')
                st.markdown(f"⏱Time : {time_5k} ")
                st.markdown(f"Pace: {pace_5k} mins/km")
        with col2:
            with st.container(border=True):
                st.markdown('**🏃 10km best effort**')
                st.markdown(f" ⏱Time : {time_10k} ")
                st.markdown(f"Pace: {pace_10k} mins/km")
        
        with col3:
            with st.container(border=True):
                st.markdown('🏃 21km best effort')
                st.markdown(f" ⏱Time : {time_21k} ")
                st.markdown(f"Pace: {pace_21k} mins/km")
        st.markdown('-------')
        
        # building the dataframe for donot graph representing the percentage of each pace zone 
        pace_counts = data_outliers['pace_zone'].value_counts().reset_index()
        pace_counts['percentage'] = round(pace_counts['count'] / pace_counts['count'].sum() * 100,2)
        
        #Count and percentage of  how many runs fall in each bin,
        # the value_counts().reset_index() gives you dataframe of with columns distance_category and counts
        
         # variables for the distance_category
        # Define bins and labels 
        bins = [0, 5, 10, 20, 30, float('inf')] 
        labels = ["1-5 km", "5-10 km", "10-20 km", "20-30 km", "30+ km"] 
        # Create distance category column 
        data_outliers["distance_category"] = pd.cut( data_outliers["distance"], bins=bins, labels=labels, right=True )
        
        
        distance_counts = data_outliers["distance_category"].value_counts().reset_index()
        distance_counts.columns = ['distance_category', 'count']
        distance_counts['distance_category'] = distance_counts['distance_category'].astype(str) # string because the color parameter takes string 
        distance_counts['percentage'] = round(distance_counts['count'] / distance_counts['count'].sum() * 100,2)
        
        st.markdown('**📈 2. Running Trends Donot** ')
        col1, col2 = st.columns(2)
        with col1:
                with st.container(border=True):
                    st.subheader("🏃 Pace Zone Distribution")
                    plost.donut_chart(
                    data=pace_counts,
                    theta='percentage',
                    color='pace_zone',
                    legend= 'right', 
                    use_container_width=True)
        with col2:
            with st.container(border=True):
                st.subheader("📏 Distance Category Distribution")
                plost.donut_chart(
                data=distance_counts,
                theta='percentage',
                color='distance_category', # string 
                legend='right', 
                use_container_width=True)
            
        # Running trends Rows 
      
        # Grouping Rows by time. We use the resample method to group rows by chunk of time.
        #resample requires the index of the dataset to be datetime_like values. 
        
        # setting index to activity_date since it is a datetime object.

        activity_date_index_df = data_outliers.set_index('activity_date').copy()
        
        time_frame_map = {
            "Weekly": "W",
            "Monthly": "M",
        }
        resample_code = time_frame_map.get(time_frame, 'W')

        # Group rows by week to calculate consistency, and applying aggregrate function to the required features.
        df_per_time_frame = activity_date_index_df.resample(resample_code).agg({
            'distance':'sum',
            'moving_mins': 'sum',
            'activity_id':'count',
            'elevation_gain': "sum",
            'avg_pace': 'mean'
        }).rename(columns={
            'activity_id': 'run_count',
            'avg_pace': 'mean_avg_pace'
            })
        df_per_time_frame['period'] = df_per_time_frame.index
        df_per_time_frame['year'] = df_per_time_frame['period'].dt.year
        # adding a cummulative sum of distances
        df_per_time_frame['Cumulative_distance'] =  df_per_time_frame['distance'].cumsum()
        
        st.markdown('----')
        st.markdown('**📈 2. Running Trends** ')
        # Tracking performances based frequency (Number of run count per week)
        
         # Plost bar chat for the number of run counts
        plost.bar_chart(
        data=df_per_time_frame,
        bar='period',
        value='run_count',
        color='year',
        width=700,
        title="Number of run counts"
        )
        
        # Plost bar chat for the Running Milleage 
        plost.bar_chart(
        data=df_per_time_frame,
        bar='period',
        value='distance',
        color='year',
        width=700,
        title="Running Milleage"
        )
        
        #PLost line chart for the average pace over time.
        st.line_chart(
        data=df_per_time_frame,
        x='period',
        y='mean_avg_pace',
        color='year'
        )
        
        #PLost line chart for the average pace over time.
        st.line_chart(
        data=df_per_time_frame,
        x='period',
        y='elevation_gain',
        color='year'
        )
        
        #plost for the scatter plot 
        st.markdown('-----')
        st.markdown("**🔵 3. Scatter Plot Analysis**")
        plost.scatter_chart(
        data=data_outliers,
        x='elevation_gain',
        y='avg_pace',
        height=500,
        title = "Scatter Plot of elevation gain vs average pace"
        )
        
        plost.scatter_chart(
        data=data_outliers,
        x='distance',
        y='avg_pace',
        height=500,
        title = "Scatter Plot of distance vs average pace"
        )
        st.markdown('---')
        
        # Time of the day preference
        st.markdown(' **⏰ 4. Time best Performance**')
        # creating a bar plot to visualize if i'm a morning runner or a evening runner. 
        # Step 2: group by hour and count the number of runs
        data_outliers['hour'] = data_outliers["activity_date"].dt.hour
        runs_per_hour = data_outliers.groupby(['hour', 'year'])['activity_id'].count().reset_index(name='run_count')
        
        plost.bar_chart(
        data=runs_per_hour,
        bar='hour',
        value='run_count',
        group='year',
        color='year',
        legend='right',
        title= 'Run by hours For each year')

        # Average pace by hours
        # Calculate the average pace for each hour of the day, grouped by year
        pace_per_hour = data_outliers.groupby(['hour', 'year'])['avg_pace'].mean().reset_index(name='mean_pace')
        
        plost.bar_chart(
        data=pace_per_hour,
        bar='hour',
        value='mean_pace',
        group='year',
        color='year',
        legend='right',
        title= 'Mean_pace by hours For each year')
        
        
        data_outliers['day_name'] = data_outliers['activity_date'].dt.day_name()
        run_by_days_frame = data_outliers.groupby(['day_name', 'year'])['activity_id'].count().reset_index(name='run_count')
        day_name_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        run_by_days_frame['day_name'] = pd.Categorical(run_by_days_frame['day_name'], categories=day_name_order, ordered=True)
        run_by_days_frame = run_by_days_frame.sort_values(['day_name', 'year'])
        
        st.write(run_by_days_frame)
        # Creating an altair bar chart 
        st.markdown('Run by days in a weeks for each year')
        st.bar_chart(
            run_by_days_frame, x="day_name", y="run_count", color="year", stack=False
        )
        
        # For the bar chart above it was better to just use st.bar_chart than the plost library,
        # becasue the plost library does not enables the order in the day_name of the week, instead
        # by default it is ordered in an alphabetical order.
    
        
        #Cumulative distance per year 
        distance_per_year = data_outliers.groupby(['year', 'month'])['distance'].sum().reset_index()
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        # ordered the month columns
        distance_per_year['month'] = (pd.Categorical(distance_per_year['month'], categories=month_order, ordered= True ))
        
        # sort values in chronological order, first by year, then by month.
        distance_per_year= distance_per_year.sort_values(['year', 'month'])
        distance_per_year['cum_distance'] = distance_per_year.groupby('year')['distance'].cumsum()
        
        #creating an altair line chart
       
        chart = alt.Chart(distance_per_year).mark_line().encode(
            x = alt.X('month', sort = month_order),
            y = alt.Y('cum_distance'),
            color = 'year',
            tooltip= ['month', 'cum_distance', 'year'],
            )
        
        #Display the chart in streamlit 
        st.markdown('Cummulative distance covered each year')
        st.altair_chart(chart, use_container_width=True)
    