import streamlit as st
import joblib
import pandas as pd

# Optional: Debugging during dev
# import os
# st.write("Current directory contents:", os.listdir())

# Load model
model = joblib.load('maternal_risk_model.pkl')

# Streamlit UI
st.title("🩺 Maternal Health Risk Predictor")

st.markdown("""
👩‍⚕️ **Predict the maternal health risk level** based on clinical indicators.

Fill in the following patient information to receive a risk assessment and recommended next steps.
""")

# User inputs
age = st.number_input("Age (years)", 10, 100, 30)
systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", 80, 200, 120)
diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg)", 50, 130, 80)
blood_sugar = st.number_input("Blood Sugar (mg/dL)", 50, 300, 100)
body_temp = st.number_input("Body Temperature (°F)", 90.0, 110.0, 98.6)
heart_rate = st.number_input("Heart Rate (bpm)", 40, 200, 75)

# Input DataFrame
input_data = pd.DataFrame(
    [[age, systolic_bp, diastolic_bp, blood_sugar, body_temp, heart_rate]],
    columns=['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
)

st.subheader("📋 Summary of Your Inputs")
st.dataframe(input_data)

# Prediction
if st.button("Predict Risk Level"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"🎯 **Predicted Maternal Risk Level:** {prediction.upper()}")

        if prediction.lower() == 'low risk':
            st.info("✅ You are currently at **low risk**. Maintain a balanced diet, stay hydrated, take prenatal vitamins, and engage in light physical activity like walking or yoga.")
        elif prediction.lower() == 'mid risk':
            st.warning("⚠️ You are at **moderate risk**. Please monitor your blood pressure, sugar levels, and heart rate regularly. Consult your doctor to review your prenatal care plan.")
        elif prediction.lower() == 'high risk':
            st.error("🚨 You are at **high risk**. Immediate medical attention is recommended. Contact your healthcare provider for a full clinical assessment.")
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
