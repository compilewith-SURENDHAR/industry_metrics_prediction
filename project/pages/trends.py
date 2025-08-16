import streamlit as st
import pandas as pd

# Import your graph plotting function
from visualisation import plot_energy_usage, plot_energy_usage_2, plot_energy_usage_1, plot_animated_energy_trend_by_load, plot_energy_trend_for_load
# Streamlit UI
def show():
    st.header("📈 Trends Visualization")

    # User Inputs
    day = st.selectbox("Select a Day", ["Any", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    load_type = st.selectbox("Select Load Type", ["Any", "Light", "Medium", "Heavy"])

    if st.button("Show Trends"):
        st.subheader("Trend Analysis")
        
        if day == "Any" and load_type == "Any":
            plot_energy_usage() 
        elif day != "Any" and load_type == "Any" :
            plot_energy_usage_1(day)
        elif day == "Any" and load_type != "Any":
            plot_energy_trend_for_load(load_type)
        else:
            plot_energy_usage_2(day,load_type)
            
    
    if st.button("compare loads"):
        fig = plot_animated_energy_trend_by_load()
        st.pyplot(fig)

