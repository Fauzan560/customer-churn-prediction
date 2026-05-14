import streamlit as st
import joblib
import pandas as pd

# 1. Load the model and columns
try:
    model = joblib.load('churn_model.pkl')
    model_cols = joblib.load('model_columns.pkl')
except:
    st.error("Model files not found! Ensure .pkl files are in the same folder.")

st.title("🛡️ Customer Churn Intelligence")

# --- SIDEBAR INPUTS ---
# --- SIDEBAR INPUTS ---
st.sidebar.header("Customer Profile")
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 1)
monthly_charges = st.sidebar.number_input("Monthly Charges ($)", 0.0, 150.0, 125.0)
total_charges = st.sidebar.number_input("Total Charges ($)", 0.0, 8000.0, 125.0)

# Added based on your Feature Importance chart
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
partner = st.sidebar.selectbox("Has Partner?", ["Yes", "No"])
payment = st.sidebar.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])

# Existing categorical inputs
contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
internet = st.sidebar.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])

# --- UPDATED LOGIC ---
if st.button("Analyze Risk Profile"):
    input_dict = {col: 0 for col in model_cols}
    
    # Numerical
    for col in model_cols:
        c = col.lower().replace("_", "")
        if c == 'tenure': input_dict[col] = tenure
        if c == 'monthlycharges': input_dict[col] = monthly_charges
        if c == 'totalcharges': input_dict[col] = total_charges
            
    # Categorical (Matching your chart exactly)
    for col in model_cols:
        if f"gender_{gender}" == col: input_dict[col] = 1
        if f"Partner_{partner}" == col: input_dict[col] = 1
        if f"PaymentMethod_{payment}" == col: input_dict[col] = 1
        if f"Contract_{contract}" == col: input_dict[col] = 1
        if f"InternetService_{internet}" == col: input_dict[col] = 1

    input_df = pd.DataFrame([input_dict])[model_cols]
    probability = model.predict_proba(input_df)[0][1]
    
    st.write(f"### Churn Probability: {round(probability * 100, 2)}%")
    # Calculate Prediction based on the standard 0.5 threshold
    prediction = 1 if probability > 0.5 else 0

    st.write(f"### Churn Probability: {round(probability * 100, 2)}%")

    # This is the part that displays the colored box
    if prediction == 1:
        st.error("🚨 RESULT: HIGH RISK")
        st.write("This customer is likely to leave. Recommend offering a loyalty discount or contract upgrade.")
    else:
        st.success("✅ RESULT: LOW RISK")
        st.write("This customer is stable. High potential for long-term retention.")