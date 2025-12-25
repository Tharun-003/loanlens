import streamlit as st

st.title("🎯 Loan Purpose")

if "loan_type" not in st.session_state:
    st.session_state["loan_type"] = None

loan_type = st.radio(
    "Choose loan type",
    ["Education", "Home", "Personal"],
    index=["Education", "Home", "Personal"].index(st.session_state["loan_type"])
    if st.session_state["loan_type"] else 0
)

if st.button("Save & Continue"):
    st.session_state["loan_type"] = loan_type
    st.success("Loan purpose saved.")
