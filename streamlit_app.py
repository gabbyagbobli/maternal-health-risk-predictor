import streamlit as st
import pandas as pd
import pickle

# Optional: Load scaler if used during training (uncomment if needed)
# with open('scaler.pkl', 'rb') as f:
#     scaler = pickle.load(f)

# Load model
with open('maternal_risk_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Page config
st.set_page_config(page_title="Maternal Risk Predictor", page_icon="🩺")

# Title and description
st.title("🩺 Maternal Health Risk Predictor")
st.markdown("""
👩‍⚕️ **Predict the maternal health risk level** based on clinical indicators.

Fill in the following patient information to receive a risk assessment and recommended next steps.
""")

# User inputs
age = st.number_input("🔢 Age (years)", 10, 100, 30)
systolic_bp = st.number_input("🩸 Systolic Blood Pressure (mmHg)", 80, 200, 120)
diastolic_bp = st.number_input("🩸 Diastolic Blood Pressure (mmHg)", 50, 130, 80)
blood_sugar = st.number_input("🍬 Blood Sugar (mg/dL)", 50, 300, 100)
body_temp = st.number_input("🌡️ Body Temperature (°F)", 90.0, 110.0, 98.6)
heart_rate = st.number_input("❤️ Heart Rate (bpm)", 40, 200, 75)

# Input DataFrame
input_data = pd.DataFrame(
    [[age, systolic_bp, diastolic_bp, blood_sugar, body_temp, heart_rate]],
    columns=['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
)

# Display user input
st.subheader("📋 Summary of Your Inputs")
st.dataframe(input_data)

# Risk level mapping (if model outputs 0, 1, 2)
labels_map = {0: 'low risk', 1: 'mid risk', 2: 'high risk'}

# Prediction
if st.button("🔍 Predict Risk Level"):
    try:
        # If you used scaling during training, uncomment this:
        # input_data = scaler.transform(input_data)

        prediction = model.predict(input_data)[0]  # numeric or string
        risk_level = labels_map.get(prediction, str(prediction)).lower()

        st.success(f"🎯 **Predicted Maternal Risk Level:** {risk_level.upper()}")

        # Conditional advice
        if risk_level == 'low risk':
            st.info("✅ You are currently at **low risk**. Maintain a balanced diet, stay hydrated, take prenatal vitamins, and engage in light physical activity.")
        elif risk_level == 'mid risk':
            st.warning("⚠️ You are at **moderate risk**. Monitor your vitals regularly and consult your doctor to review your prenatal care plan.")
        elif risk_level == 'high risk':
            st.error("🚨 You are at **high risk**. Seek **immediate medical attention**. Contact your healthcare provider urgently.")
        else:
            st.warning("🤔 Unable to determine a specific risk level.")

    except Exception as e:
        st.error("❌ Prediction failed. Please check your inputs or contact support.")
        st.code(f"{e}", language="bash")
        st.write("📦 Input data that caused error:")
        st.dataframe(input_data)

# Footer
st.markdown("---")
st.caption("🔬 Built with ❤️ by Group 1 of Health Informatics class — Department of Statistics & Actuarial Science, University of Ghana.\n📌 For educational use only. Not a substitute for professional medical advice.")
