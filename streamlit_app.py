import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("maternal_risk_model.pkl")

# Define mapping if the model predicts 0, 1, or 2
risk_map = {0: "Low Risk", 1: "Mid Risk", 2: "High Risk"}

# Streamlit App
st.title("Maternal Health Risk Predictor")

st.markdown("Enter the following health indicators:")

# Input fields
age = st.number_input("Age", min_value=10, max_value=100, value=30)
bp = st.number_input("Systolic Blood Pressure (e.g. 130)", value=120.0)
bs = st.number_input("Blood Sugar Level", value=85.0)
body_temp = st.number_input("Body Temperature (°F)", value=98.6)
heart_rate = st.number_input("Heart Rate", value=75.0)

if st.button("Predict Risk"):
    input_data = np.array([[age, bp, bs, body_temp, heart_rate]])
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Maternal Risk Level: **{risk_map.get(prediction, 'Unknown')}**")
