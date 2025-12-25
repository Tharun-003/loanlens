import streamlit as st

st.set_page_config(
    page_title="Loan Advisory System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Loan Advisory & Risk Analysis System")

st.markdown("""
Welcome to the **Loan Advisory System**.

This application analyses your profile and loan requirements to:
- Assess **risk level**
- Predict **eligibility**
- Suggest **suitable loan products from banks**

⚠️ *This is a predictive advisory system for educational purposes only.*
""")

st.divider()

st.info("Use the navigation menu on the left to start the process.")
