import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Model load karo
with open('../models/churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../models/features.pkl', 'rb') as f:
    feature_names = pickle.load(f)

st.set_page_config(page_title="Customer Churn Predictor", page_icon="📊")
st.title("📊 Customer Churn Prediction")
st.write("Customer details bharo aur predict karo ki woh churn karega ya nahi!")

# Input fields
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    monthly_charges = st.slider("Monthly Charges ($)", 18, 119, 65)
    total_charges = st.number_input("Total Charges ($)", 0.0, 9000.0, 500.0)
    senior_citizen = st.selectbox("Senior Citizen?", [0, 1])
    gender = st.selectbox("Gender", ["Male", "Female"])
    partner = st.selectbox("Partner?", ["Yes", "No"])
    dependents = st.selectbox("Dependents?", ["Yes", "No"])

with col2:
    phone_service = st.selectbox("Phone Service?", ["Yes", "No"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])
    paperless_billing = st.selectbox("Paperless Billing?", ["Yes", "No"])
    tech_support = st.selectbox("Tech Support?", ["Yes", "No", "No internet service"])
    online_security = st.selectbox("Online Security?", ["Yes", "No", "No internet service"])

# Predict button
if st.button("🔮 Predict Churn"):
    # Input dict banao
    input_dict = {f: 0 for f in feature_names}

    input_dict['tenure'] = tenure
    input_dict['MonthlyCharges'] = monthly_charges
    input_dict['TotalCharges'] = total_charges
    input_dict['SeniorCitizen'] = senior_citizen

    if gender == "Male": input_dict['gender_Male'] = 1
    if partner == "Yes": input_dict['Partner_Yes'] = 1
    if dependents == "Yes": input_dict['Dependents_Yes'] = 1
    if phone_service == "Yes": input_dict['PhoneService_Yes'] = 1
    if internet_service == "Fiber optic": input_dict['InternetService_Fiber optic'] = 1
    if internet_service == "No": input_dict['InternetService_No'] = 1
    if contract == "One year": input_dict['Contract_One year'] = 1
    if contract == "Two year": input_dict['Contract_Two year'] = 1
    if payment_method == "Electronic check": input_dict['PaymentMethod_Electronic check'] = 1
    if payment_method == "Mailed check": input_dict['PaymentMethod_Mailed check'] = 1
    if payment_method == "Credit card (automatic)": input_dict['PaymentMethod_Credit card (automatic)'] = 1
    if paperless_billing == "Yes": input_dict['PaperlessBilling_Yes'] = 1
    if tech_support == "Yes": input_dict['TechSupport_Yes'] = 1
    if tech_support == "No internet service": input_dict['TechSupport_No internet service'] = 1
    if online_security == "Yes": input_dict['OnlineSecurity_Yes'] = 1
    if online_security == "No internet service": input_dict['OnlineSecurity_No internet service'] = 1

    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.divider()
    if prediction == 1:
        st.error(f"⚠️ Customer CHURN karega! (Probability: {probability:.1%})")
    else:
        st.success(f"✅ Customer NAHI jayega! (Probability: {probability:.1%})")