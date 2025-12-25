import streamlit as st

st.title("💳 Personal Loan Details")

income = st.number_input("Monthly Income", min_value=0)
age = st.number_input("Age", min_value=23, max_value=65)
credit = st.selectbox("Credit Score", ["Low", "Medium", "High"])
employment = st.selectbox("Employment Stability", ["Low", "Medium", "High"])

if st.button("Save & Continue"):
    st.session_state["income"] = income
    st.session_state["age"] = age
    st.session_state["credit_score"] = credit
    st.session_state["employment_stability"] = employment
    st.success("Saved. Continue ➡️")
