import streamlit as st
import pandas as pd
import pickle

# --- Custom CSS for a Nicer Look and Persistent Footer ---
st.markdown("""
<style>
    /* Main body styling */
    body {
        background-color: #f0f2f6; /* Light grey background */
    }

    /* Customizing the main title */
    .stApp > header {
        background-color: #00000000; /* Transparent header background */
    }

    h1 {
        color: #0056b3; /* Darker blue for title */
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Subheaders */
    h2 {
        color: #004085; /* Slightly lighter blue for subheaders */
        font-family: 'Segoe UI', sans-serif;
    }

    /* Main description text */
    .stMarkdown {
        text-align: center;
        font-size: 1.1rem;
        color: #333333;
    }

    /* Input labels */
    .stNumberInput > label {
        font-weight: bold;
        color: #495057;
    }

    /* Buttons */
    .stButton > button {
        background-color: #28a745; /* Green button */
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #218838; /* Darker green on hover */
        transform: translateY(-2px);
    }

    /* Prediction success/warning/error messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        font-size: 1.1rem;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-color: #ffeeba;
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-color: #f5c6cb;
    }

    /* Custom Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #e9ecef; /* Light grey background for footer */
        color: #6c757d; /* Dark grey text */
        text-align: center;
        padding: 10px;
        font-size: 0.85rem;
        border-top: 1px solid #dee2e6;
        z-index: 1000; /* Ensure it's above other content */
    }
</style>
""", unsafe_allow_html=True)

# --- Load Model and Scaler ---
# Make sure 'maternal_risk_model.pkl' and 'scaler.pkl' are in the same directory
# as your Streamlit app script, or provide the full path.
try:
    with open('maternal_risk_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    st.error("Error: Model or scaler files not found. Please ensure 'maternal_risk_model.pkl' and 'scaler.pkl' are in the correct directory.")
    st.stop() # Stop the app if files aren't found

# --- Page Configuration ---
st.set_page_config(page_title="Maternal Risk Predictor", page_icon="🩺", layout="centered")

# --- Title and Description ---
st.title("🩺 Maternal Health Risk Predictor")
st.markdown("""
👩‍⚕️ **Predict your maternal health risk level** based on key clinical indicators.

Simply fill in the patient information below to receive a personalized risk assessment and recommended next steps.
""")

st.write("---") # Visual separator

# --- User Inputs in Columns for Better Layout ---
st.subheader("📝 Enter Patient Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🔢 **Age (years)**", 10, 100, 30, help="Patient's age in years.")
    systolic_bp = st.number_input("🩸 **Systolic Blood Pressure (mmHg)**", 80, 200, 120, help="Top number in blood pressure reading.")
    blood_sugar = st.number_input("🍬 **Blood Sugar (mg/dL)**", 50, 300, 100, help="Blood glucose level.")

with col2:
    diastolic_bp = st.number_input("🩸 **Diastolic Blood Pressure (mmHg)**", 50, 130, 80, help="Bottom number in blood pressure reading.")
    body_temp = st.number_input("🌡️ **Body Temperature (°F)**", 90.0, 110.0, 98.6, format="%.1f", help="Patient's body temperature.")
    heart_rate = st.number_input("❤️ **Heart Rate (bpm)**", 40, 200, 75, help="Patient's heart rate in beats per minute.")

# --- Prepare Input Data ---
# Note: input_data and input_scaled were outside the button logic in your original code.
# They should be defined *after* the user inputs are collected.
input_data = pd.DataFrame(
    [[age, systolic_bp, diastolic_bp, blood_sugar, body_temp, heart_rate]],
    columns=['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
)

st.write("---") # Visual separator

# --- Display User Input Summary ---
st.subheader("📋 Summary of Your Entered Data")
st.dataframe(input_data.style.set_properties(**{'background-color': '#e6f7ff', 'color': '#333333', 'border-color': '#a8d8ea'}))

# --- Risk Level Mapping ---
labels_map = {0: 'low risk', 1: 'mid risk', 2: 'high risk'}

# --- Prediction ---
st.write("---") # Visual separator
st.markdown("<h2 style='text-align: center; color: #004085;'>Ready for Your Risk Assessment?</h2>", unsafe_allow_html=True)
if st.button("🔍 **Predict Risk Level**", use_container_width=True):
    with st.spinner("Analyzing data..."):
        try:
            # Ensure input is scaled before prediction
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)[0]
            risk_level = labels_map.get(prediction, str(prediction)).lower()

            st.markdown("---") # Visual separator

            if risk_level == 'low risk':
                st.success(f"🎯 **Predicted Maternal Risk Level: {risk_level.upper()}**")
                st.info("✅ You are currently at **low risk**. Maintain a balanced diet, stay hydrated, take prenatal vitamins, and engage in light physical activity. Continue with your regular prenatal check-ups.")
            elif risk_level == 'mid risk':
                st.warning(f"🎯 **Predicted Maternal Risk Level: {risk_level.upper()}**")
                st.warning("⚠️ You are at **moderate risk**. It's important to monitor your vitals regularly. Please consult your doctor to review your prenatal care plan and discuss any concerns.")
            elif risk_level == 'high risk':
                st.error(f"🚨 **Predicted Maternal Risk Level: {risk_level.upper()}**")
                st.error("🚨 You are at **high risk**. Please **seek immediate medical attention**. Contact your healthcare provider urgently or visit the nearest emergency department.")
            else:
                st.warning("🤔 Unable to determine a specific risk level. Please verify your inputs.")

        except Exception as e:
            st.error("❌ Prediction failed. An unexpected error occurred. Please check your inputs or contact support.")
            st.code(f"Error details: {e}", language="bash")
            st.write("📦 Input data that caused the error:")
            st.dataframe(input_data)

# --- Persistent Custom Footer ---
# Using markdown with unsafe_allow_html=True to inject the custom footer div
st.markdown(
    """
    <div class="footer">
        <p>🔬 Built with ❤️ by Group 1 of Health Informatics class — Department of Statistics & Actuarial Science, University of Ghana.</p>
        <p>🙏 Special thanks to our lecturer, Dr. Eric Nyarko (MPh, PhD).</p>
        <p>📌 For educational use only. Not a substitute for professional medical advice.</p>
    </div>
    """,
    unsafe_allow_html=True
)
