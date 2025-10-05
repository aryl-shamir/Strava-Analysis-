import sys
from pathlib import Path
import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # The listin which python retrieve modules, and we add to that the parent directory path. 
from scripts.cleaning_data import clean_data

def strav_data(data_file):
    
    st.subheader("Strava Analysis app")
    st.markdown("Analysing your running strava data, and predicting your next pace run")
    #Display the dataset 
    st.subheader('1. Strava Dataset')
    
    # creating a session state variable for the dataframe
    if not data_file:
        if "dataframe" not in st.session_state:
            st.session_state.dataframe = None 
        st.info('Awaiting for CSV file to be uploaded.')
    else:
        with st.expander('See Strava Dataframe'):
            st.session_state.dataframe = pd.read_csv(data_file)
            st.dataframe(st.session_state.dataframe)

    # Cleaning the dataset. 
    if "clean_data" not in st.session_state:
        st.session_state.clean_data = False
    if "clean_data_results" not in st.session_state:
        st.session_state.clean_data_results = None
        
    def on_click_clean_data():
        """Update the session state variable of the clean_data button to True, and store the result 
         in the session state clean_data result. """
        
        st.session_state.clean_data = True 
        
        data_with_outliers, data_with_no_outliers = clean_data(df=st.session_state.dataframe)
        st.session_state.clean_data_results = data_with_no_outliers
        
    # creating the clean data button
    st.button('clean_data', on_click=on_click_clean_data)
    
    #ckeck the session state variable of the clean_data button using the if conditiaml statement. 
    if st.session_state.clean_data: # This is True when you click on the clean_data button
        with st.expander('See Clean DataFrame'):
            st.dataframe(st.session_state.clean_data_results)


# if __name__ == "__main__":
#     main()