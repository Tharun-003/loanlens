import streamlit as st

st.title("🏠 Home Loan Details")

property_value = st.number_input("Property Value", min_value=0)
income = st.number_input("Monthly Income", min_value=0)
credit = st.selectbox("Credit Score", ["Low", "Medium", "High"])
age = st.number_input("Age", min_value=21, max_value=65)

if st.button("Save & Continue"):
    st.session_state["property_value"] = property_value
    st.session_state["income"] = income
    st.session_state["credit_score"] = credit
    st.session_state["age"] = age
    st.success("Saved. Continue ➡️")
