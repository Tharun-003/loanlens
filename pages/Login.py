import streamlit as st

st.title("🔐 User Login")

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "user_bank" not in st.session_state:
    st.session_state["user_bank"] = ""

name = st.text_input("User Name", value=st.session_state["user_name"])
bank = st.selectbox(
    "Select Bank",
    ["SBI", "HDFC", "ICICI", "Axis"],
    index=["SBI", "HDFC", "ICICI", "Axis"].index(st.session_state["user_bank"])
    if st.session_state["user_bank"] else 0
)

if st.button("Continue"):
    st.session_state["user_name"] = name
    st.session_state["user_bank"] = bank
    st.success("Login saved. Use sidebar to continue ➡️")
