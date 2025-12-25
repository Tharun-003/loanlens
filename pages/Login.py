import streamlit as st

st.title("🔐 User Login")

name = st.text_input("User Name")
account = st.text_input("Account Number")
bank = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis"])

if st.button("Continue"):
    if name and account:
        st.session_state["user_name"] = name
        st.session_state["user_bank"] = bank
        st.success("Login successful. Proceed using sidebar ➡️")
    else:
        st.error("Please fill all fields.")
