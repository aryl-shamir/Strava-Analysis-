import sys
from pathlib import Path

import streamlit as st 
from streamlit_option_menu import option_menu

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    
from clean_data_app import strav_data
from streamlit_app.dashboard import dash_bord

# web interface.
def main():
    
    st.logo(image='static/Strava image.png', size="large")
    
    
    # Upload CSV data 
    with st.sidebar.header("1. Upload your strava csv data"):
        uploaded_file = st.sidebar.file_uploader("upload your strava_csv file", type="csv")
        selected = option_menu(
            menu_title="Main Menu",
            options=["clean_data", "dash_boards", "Forecasting_Analysis"],
            icons = ['clipboard-data', 'bar-chart-line-fill', 'graph-up'],
            menu_icon= "cast", # icons taken form Bootstraps icons website 
    )
        time_frame = st.sidebar.selectbox("Select time frame (only concerns the 📈 2. Running Trends)",
                              ("Weekly", "Monthly")
    )
        
   
    if selected == "clean_data":
        strav_data(data_file=uploaded_file)
    if selected == "dash_boards":
        dash_bord(data_file=uploaded_file, time_frame=time_frame)


if __name__ == "__main__":
    main()
