import streamlit as st

st.title("💳 Personal Loan Details")

for key, default in {
    "age": 25,
    "income": 25000,
    "credit_score": "Medium",
    "employment_stability": "Medium"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

age = st.number_input("Age", value=st.session_state["age"], min_value=23)
income = st.number_input("Monthly Income", value=st.session_state["income"])
credit = st.selectbox(
    "Credit Score",
    ["Low", "Medium", "High"],
    index=["Low", "Medium", "High"].index(st.session_state["credit_score"])
)
employment = st.selectbox(
    "Employment Stability",
    ["Low", "Medium", "High"],
    index=["Low", "Medium", "High"].index(st.session_state["employment_stability"])
)

if st.button("Save & Continue"):
    st.session_state["age"] = age
    st.session_state["income"] = income
    st.session_state["credit_score"] = credit
    st.session_state["employment_stability"] = employment
    st.success("Personal loan details saved.")
