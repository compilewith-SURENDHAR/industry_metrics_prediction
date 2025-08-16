import streamlit as st
from pages import energy_estimation, co2_estimation, trends

# Set page config
st.set_page_config(
    page_title="Energy Estimation Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Title and description
st.title("⚡ Energy Consumption Analysis Dashboard")
st.markdown("Analyze and predict energy consumption and CO2 emissions")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Select a Page",
    ["Energy Estimation", "CO2 Estimation", "Trends Visualization"]
)

# Page routing
if page == "Energy Estimation":
    energy_estimation.show()
elif page == "CO2 Estimation":
    co2_estimation.show()
else:
    trends.show()