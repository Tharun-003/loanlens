import streamlit as st

st.title("📄 Loan History")

loan_amount = st.number_input("Required Loan Amount", min_value=0)
existing = st.radio("Existing Loan?", ["Yes", "No"])

emi_delay = "Never"
if existing == "Yes":
    emi_delay = st.selectbox(
        "Past EMI Delays",
        ["Never", "Sometimes", "Frequent"]
    )

if st.button("Save & Continue"):
    st.session_state["loan_amount"] = loan_amount
    st.session_state["existing_loan"] = existing
    st.session_state["emi_delay"] = emi_delay
    st.success("Saved. Continue ➡️")
