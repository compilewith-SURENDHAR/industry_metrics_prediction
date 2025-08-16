import streamlit as st
import joblib
import pandas as pd

# Load CO2 emission prediction model
with open("models/co2_emission_prediction.pkl", "rb") as file:
    co2_model = joblib.load(file)

# Function to preprocess inputs
def preprocess_inputs(energy_consumption, load_type):
    # Encode Load Type (Light=0, Medium=1, Heavy=2)
    load_mapping = {"Light": 0, "Medium": 1, "Heavy": 2}
    load_type_encoded = load_mapping[load_type]

    # Ensure the column name matches the model's expected feature name
    input_data = pd.DataFrame([[energy_consumption, load_type_encoded]], columns=["Usage_kWh", "Load_Type"])

    return input_data

# Function to predict CO₂ emission
def predict_co2(input_data):
    co2_output = co2_model.predict(input_data)
    return co2_output[0]

# Streamlit UI
def show():
    st.header("🌍 CO₂ Emission Estimation")

    # User Inputs
    energy_consumption = st.number_input("Enter Energy Consumption (kWh)", min_value=0.0, step=0.1)
    load_type = st.selectbox("Select Load Type", ["Light", "Medium", "Heavy"])

    if st.button("Estimate CO₂ Emission"):
        # Preprocess input
        input_data = preprocess_inputs(energy_consumption, load_type)

        # Get prediction
        co2_emission = predict_co2(input_data)
        if co2_emission<=0:
            co2_emission = 0

        # Display result
        st.subheader("Predicted CO₂ Emission:")
        st.write(f"🌱 {co2_emission:.6f} tonne CO₂")
