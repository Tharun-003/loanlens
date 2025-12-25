import streamlit as st

st.title("🎯 Select Loan Purpose")

loan_type = st.radio(
    "Choose loan type",
    ["Education", "Home", "Personal"]
)

if st.button("Next"):
    st.session_state["loan_type"] = loan_type
    st.success("Loan type selected. Continue ➡️")
