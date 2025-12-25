import streamlit as st

st.title("🏠 Home Loan Details")

for key, default in {
    "age": 25,
    "income": 30000,
    "credit_score": "Medium"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

age = st.number_input("Age", value=st.session_state["age"], min_value=21)
income = st.number_input("Monthly Income", value=st.session_state["income"])
credit = st.selectbox(
    "Credit Score",
    ["Low", "Medium", "High"],
    index=["Low", "Medium", "High"].index(st.session_state["credit_score"])
)

if st.button("Save & Continue"):
    st.session_state["age"] = age
    st.session_state["income"] = income
    st.session_state["credit_score"] = credit
    st.success("Home loan details saved.")
