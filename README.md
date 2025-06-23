# Maternal Health Risk Predictor

[![Deploy with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/gabbyagbobli/maternal-health-risk-predictor/main/streamlit_app.py)

## 📋 Overview
This is a machine learning web app built with **Streamlit** that predicts the maternal health risk level of a patient based on key health indicators using a **Naive Bayes classifier** trained in Google Colab.

## 🔍 Input Features
- Age
- Systolic Blood Pressure
- Blood Sugar
- Body Temperature
- Heart Rate

## 🎯 Prediction Output
- Low Risk
- Mid Risk
- High Risk

## 🚀 How to Run the App Locally

1. **Clone the repository:**
```
git clone https://github.com/gabbyagbobli/maternal-health-risk-predictor.git
cd maternal-health-risk-predictor
```

2. **Install dependencies:**
```
pip install -r requirements.txt
```

3. **Run the app:**
```
streamlit run streamlit_app.py
```

## 📦 Model Details

- The app uses a **Gaussian Naive Bayes model**
- Trained using `scikit-learn`
- Model is saved as `maternal_risk_model.pkl` and included in this repository

## 🛠 Technologies Used

- Python
- Streamlit
- scikit-learn
- pandas
- NumPy
- Google Colab

## 👨🏽‍💻 Author

**Gabby Agbobli**  
GitHub: [gabbyagbobli](https://github.com/gabbyagbobli)

## 📄 License

This project is licensed under the MIT License.