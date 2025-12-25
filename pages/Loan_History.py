import streamlit as st

st.title("📄 Loan History")

for key, default in {
    "existing_loan": "No",
    "emi_delay": "Never",
    "data_complete": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

existing = st.radio(
    "Existing Loan?",
    ["Yes", "No"],
    index=0 if st.session_state["existing_loan"] == "Yes" else 1
)

emi_delay = st.session_state["emi_delay"]
if existing == "Yes":
    emi_delay = st.selectbox(
        "Past EMI Delays",
        ["Never", "Sometimes", "Frequent"],
        index=["Never", "Sometimes", "Frequent"].index(st.session_state["emi_delay"])
    )

if st.button("Save & Continue"):
    st.session_state["existing_loan"] = existing
    st.session_state["emi_delay"] = emi_delay
    st.session_state["data_complete"] = True
    st.success("Loan history saved.")
