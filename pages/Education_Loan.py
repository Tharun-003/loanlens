import streamlit as st

st.title("🎓 Education Loan Details")

admission = st.radio("Admission Confirmed?", ["Yes", "No"])
coapplicant = st.radio("Co-applicant Available?", ["Yes", "No"])
age = st.number_input("Age", min_value=16, max_value=40)

if st.button("Save & Continue"):
    st.session_state["admission_confirmed"] = admission
    st.session_state["coapplicant"] = coapplicant
    st.session_state["age"] = age
    st.success("Saved. Continue ➡️")
