import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# Load models
with open("models/multi_output_model.pkl", "rb") as file:
    multi_model = joblib.load(file)

with open("models/energy_estimation.pkl", "rb") as file:
    energy_model = joblib.load(file)


# Function to preprocess inputs
def preprocess_inputs(day, load_type, start_time, end_time, month):
    
    # Validate time (ensure it's exactly 1 hour)
    start_hour = start_time.hour
    end_hour = end_time.hour
    if end_hour - start_hour != 1:
        st.error("Please select a 1-hour time range.")
        return None

    # Encode Load Type (Light=0, Medium=1, Heavy=2)
    load_mapping = {"Light": 0, "Medium": 1, "Heavy": 2}
    load_type_encoded = load_mapping[load_type]

    # Calculate WeekStatus
    weekstatus = 1 if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] else 0

    day_features = [
    "Day_Of_Week_Monday", "Day_Of_Week_Saturday", "Day_Of_Week_Sunday",
    "Day_Of_Week_Thursday", "Day_Of_Week_Tuesday", "Day_Of_Week_Wednesday"]

    # One-hot encoding for Day of Week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"]
    day_encoding = {f"Day_Of_Week_{d}": 1 if d == day else 0 for d in days}

    # Ensure the dictionary follows the desired order
    day_encoding = {key: day_encoding.get(key, 0) for key in day_features}
        
    # Calculate NSM (Seconds from Midnight)
    nsm = start_hour * 3600

    # Prepare data for the first model
    input_data = {
        "Month": month,
        "WeekStatus": weekstatus,
        "NSM": nsm,
        "Load_Type": load_type_encoded,
        "Hour": start_hour,
        **day_encoding
    }

    return input_data


def predict_energy_consumption(input_data):
    # Convert input_data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict first 4 parameters
    preds = multi_model.predict(input_df)

    # Prepare input for final model (without NSM)
    final_input = input_df.copy()
    del final_input["NSM"]
    final_input["Lagging_Current_Reactive.Power_kVarh"] = preds[0][0]
    final_input["Leading_Current_Reactive_Power_kVarh"] = preds[0][1]
    final_input["Lagging_Current_Power_Factor"] = preds[0][2]
    final_input["Leading_Current_Power_Factor"] = preds[0][3]

    # Predict energy consumption
    energy_pred = energy_model.predict(final_input)

    return preds[0], energy_pred[0]

# Streamlit UI
def show():
    st.header("⚡ Energy Estimation")

    # User Inputs
    day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    load_type = st.selectbox("Select Load Type", ["Light", "Medium", "Heavy"])
    start_time = st.time_input("Select Start Time")
    end_time = st.time_input("Select End Time")
    month = st.selectbox("Select Month", list(range(1, 13)))

    if st.button("Estimate Energy"):
        # Preprocess input
        input_data = preprocess_inputs(day, load_type, start_time, end_time, month)

        if input_data:
            # Get predictions
            power_factors, energy_output = predict_energy_consumption(input_data)

            # Display results
            st.subheader("Predicted Parameters:")
            st.write(f"Lagging Current Reactive Power: {power_factors[0]:.2f} kVarh")
            st.write(f"Leading Current Reactive Power: {power_factors[1]:.2f} kVarh")
            st.write(f"Lagging Current Power Factor: {power_factors[2]:.2f}")
            st.write(f"Leading Current Power Factor: {power_factors[3]:.2f}")

            st.subheader("Estimated Energy Consumption:")
            st.write(f"🔋 {energy_output:.2f} kWh")
