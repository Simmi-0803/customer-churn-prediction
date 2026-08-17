import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Churn Predictor", layout="centered")

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('columns.pkl', 'rb') as f:
        columns = pickle.load(f)
    return model, columns

model, columns = load_model()

st.title("Customer Churn Predictor")
st.caption("Balanced Logistic Regression — optimised for recall on the churn class")

col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    monthly = st.number_input("Monthly Charges", 18.0, 120.0, 65.0)
    total = st.number_input("Total Charges", 0.0, 9000.0, 800.0)
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    payment = st.selectbox("Payment Method", [
        "Bank transfer (automatic)", "Credit card (automatic)",
        "Electronic check", "Mailed check"])

with col2:
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])
    phone = st.selectbox("Phone Service", ["No", "Yes"])
    paperless = st.selectbox("Paperless Billing", ["No", "Yes"])

st.markdown("**Support add-ons**")
c1, c2, c3 = st.columns(3)
with c1:
    online_sec = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    online_bak = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
with c2:
    device = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
    tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
with c3:
    tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
    movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
    multi = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

if st.button("Predict", type="primary"):
    row = pd.DataFrame(0, index=[0], columns=columns)

    row['tenure'] = tenure
    row['MonthlyCharges'] = monthly
    row['TotalCharges'] = total
    row['gender'] = 1 if gender == "Male" else 0
    row['SeniorCitizen'] = 1 if senior == "Yes" else 0
    row['Partner'] = 1 if partner == "Yes" else 0
    row['Dependents'] = 1 if dependents == "Yes" else 0
    row['PhoneService'] = 1 if phone == "Yes" else 0
    row['PaperlessBilling'] = 1 if paperless == "Yes" else 0

    def set_dummy(prefix, value):
        col = f"{prefix}_{value}"
        if col in row.columns:
            row[col] = 1

    set_dummy("Contract", contract)
    set_dummy("InternetService", internet)
    set_dummy("PaymentMethod", payment)
    set_dummy("OnlineSecurity", online_sec)
    set_dummy("OnlineBackup", online_bak)
    set_dummy("DeviceProtection", device)
    set_dummy("TechSupport", tech)
    set_dummy("StreamingTV", tv)
    set_dummy("StreamingMovies", movies)
    set_dummy("MultipleLines", multi)

    prob = model.predict_proba(row)[0][1]

    if prob < 0.3:
        band, colour = "Low", "green"
    elif prob < 0.6:
        band, colour = "Medium", "orange"
    else:
        band, colour = "High", "red"

    st.markdown("---")
    m1, m2 = st.columns(2)
    m1.metric("Churn Probability", f"{prob:.1%}")
    m2.markdown(f"### Risk Band: :{colour}[{band}]")

    contrib = row.iloc[0].values * model.coef_[0]
    drivers = pd.DataFrame({
        'feature': columns,
        'contribution': contrib
    })

    up = drivers[drivers['contribution'] > 0].sort_values('contribution', ascending=False).head(5)
    down = drivers[drivers['contribution'] < 0].sort_values('contribution').head(5)

    st.markdown("---")
    d1, d2 = st.columns(2)

    with d1:
        st.markdown("**Pushing toward churn**")
        if len(up):
            st.dataframe(up.set_index('feature').round(3), width='stretch')
        else:
            st.write("None")

    with d2:
        st.markdown("**Pushing away from churn**")
        if len(down):
            st.dataframe(down.set_index('feature').round(3), width='stretch')
        else:
            st.write("None")

    st.caption("Contribution = feature value x model coefficient. Positive increases churn risk.")