import streamlit as st
import pandas as pd
import requests

# Title of the app
st.title("Customer Churn Prediction")

# Input form
age = st.number_input("Age", min_value=18, max_value=100, value=30)
gender = st.selectbox("Gender", ["Male", "Female"])
tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
usage_frequency = st.number_input("Usage Frequency", min_value=0, max_value=100, value=20)
support_calls = st.number_input("Support Calls", min_value=0, max_value=20, value=2)
payment_delay = st.number_input("Payment Delay (Days)", min_value=0, max_value=60, value=5)
subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
contract_length = st.selectbox("Contract Length", ["Monthly", "Quarterly", "Annual"])
total_spend = st.number_input("Total Spend", min_value=0, max_value=10000, value=500)
last_interaction = st.number_input("Last Interaction (Days)", min_value=0, max_value=100, value=15)

# Prediction button
if st.button("Predict"):
    # Create input data dictionary
    input_data = {
        "age": age,
        "gender": gender,
        "tenure": tenure,
        "usage_frequency": usage_frequency,
        "support_calls": support_calls,
        "payment_delay": payment_delay,
        "subscription_type": subscription_type,
        "contract_length": contract_length,
        "total_spend": total_spend,
        "last_interaction": last_interaction
    }

    try:
        print("Sending request to:", "http://127.0.0.1:8000/predict")
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        prediction = response.json()

        # Display prediction
        st.write(f"Prediction: **{prediction['prediction']}**")  # Accessing the 'prediction' key

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")