import streamlit as st

st.title("🎓 Education Loan Details")

for key, default in {
    "age": 18,
    "admission_confirmed": "Yes",
    "coapplicant": "Yes"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

age = st.number_input("Age", value=st.session_state["age"], min_value=16)
admission = st.radio(
    "Admission Confirmed?",
    ["Yes", "No"],
    index=0 if st.session_state["admission_confirmed"] == "Yes" else 1
)
coapplicant = st.radio(
    "Co-applicant Available?",
    ["Yes", "No"],
    index=0 if st.session_state["coapplicant"] == "Yes" else 1
)

if st.button("Save & Continue"):
    st.session_state["age"] = age
    st.session_state["admission_confirmed"] = admission
    st.session_state["coapplicant"] = coapplicant
    st.success("Education loan details saved.")
