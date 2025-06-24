import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open('maternal_risk_model.pkl', 'rb'))

# Streamlit app
st.title("Maternal Health Risk Predictor")

st.markdown(
    """
    Enter the following health indicators to predict the maternal risk level.
    """
)

# User inputs
age = st.number_input("Age", min_value=10, max_value=100, value=30)
systolic_bp = st.number_input("Systolic Blood Pressure", min_value=80, max_value=200, value=120)
diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=50, max_value=130, value=80)
blood_sugar = st.number_input("Blood Sugar (BS)", min_value=50, max_value=300, value=100)
body_temp = st.number_input("Body Temperature (°F)", min_value=90.0, max_value=110.0, value=98.6)
heart_rate = st.number_input("Heart Rate", min_value=40, max_value=200, value=75)

# Prepare input as DataFrame
input_data = pd.DataFrame(
    [[age, systolic_bp, diastolic_bp, blood_sugar, body_temp, heart_rate]],
    columns=['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
)

# Predict and display result
if st.button("Predict Risk Level"):
    prediction = model.predict(input_data)[0]
    
    st.success(f"Predicted Maternal Risk Level: **{prediction}**")

    # Provide tailored advice
    if prediction.lower() == 'low risk':
        st.info("✅ You are currently at **low risk**. Maintain a balanced diet, take prenatal vitamins, and engage in light physical activity like walking or yoga.")
    elif prediction.lower() == 'mid risk':
        st.warning("⚠️ You are at **moderate risk**. It's advisable to monitor your vitals regularly and consult your healthcare provider for tailored guidance.")
    elif prediction.lower() == 'high risk':
        st.error("🚨 You are at **high risk**. Please consult your doctor immediately for a comprehensive checkup and monitoring plan.")
