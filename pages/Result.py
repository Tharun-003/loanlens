# -------------------------------------------------
# FORCE PROJECT ROOT INTO PYTHON PATH (CRITICAL)
# -------------------------------------------------
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# IMPORTS
# -------------------------------------------------
import streamlit as st

from logic.risk_analaysis import calculate_risk
from logic.rule_eligibility import rule_based_eligibility
from logic.bank_matcher import recommend_loans
from logic.explanation_engine import (
    generate_risk_explanation,
    generate_eligibility_explanation,
    generate_bank_match_explanation,
    generate_improvement_tips
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Result", page_icon="📊", layout="centered")

st.title("📊 Loan Advisory Result")

# -------------------------------------------------
# SAFETY CHECK: DID USER COMPLETE PREVIOUS STEPS?
# -------------------------------------------------
if not st.session_state.get("data_complete", False):
    st.error("Please complete all previous steps before viewing results.")
    st.stop()

# -------------------------------------------------
# BUILD USER PROFILE (READ-ONLY)
# -------------------------------------------------
user_profile = {
    "loan_type": st.session_state.get("loan_type"),
    "age": st.session_state.get("age"),
    "income": st.session_state.get("income"),
    "credit_score": st.session_state.get("credit_score"),
    "employment_stability": st.session_state.get("employment_stability", "Medium"),
    "existing_loan": st.session_state.get("existing_loan"),
    "emi_delay": st.session_state.get("emi_delay"),
    "coapplicant": st.session_state.get("coapplicant", "No"),
    "admission_confirmed": st.session_state.get("admission_confirmed", "No"),
}

# -------------------------------------------------
# 3️⃣ RISK ANALYSIS
# -------------------------------------------------
risk_level = calculate_risk(user_profile)
risk_explanation = generate_risk_explanation(user_profile, risk_level)

risk_color = {
    "Low": "🟢",
    "Medium": "🟡",
    "High": "🔴"
}[risk_level]

st.subheader("🚦 Risk Analysis")
st.markdown(f"**Risk Level:** {risk_color} **{risk_level}**")
st.caption(risk_explanation)

st.divider()

# -------------------------------------------------
# 4️⃣ RULE-BASED ELIGIBILITY
# -------------------------------------------------
eligibility = rule_based_eligibility(user_profile, risk_level)
eligibility_explanation = generate_eligibility_explanation(
    user_profile["loan_type"], eligibility
)

eligibility_color = {
    "Eligible": "🟢",
    "Borderline": "🟡",
    "Not Eligible": "🔴"
}[eligibility]

st.subheader("✅ Eligibility Status")
st.markdown(f"**Status:** {eligibility_color} **{eligibility}**")
st.caption(eligibility_explanation)

st.divider()

# -------------------------------------------------
# 5️⃣ BANK & LOAN RECOMMENDATION
# -------------------------------------------------
st.subheader("🏦 Recommended Loan Options")

if eligibility == "Not Eligible":
    st.warning("Based on current details, loan recommendations are not shown.")
else:
    recommended_loans = recommend_loans(
        user_profile=user_profile,
        user_risk=risk_level
    )

    if not recommended_loans:
        st.info("No suitable loan products found for the given profile.")
    else:
        for loan in recommended_loans:
            with st.container(border=True):
                st.markdown(f"### {loan['bank_name']} — {loan['loan_name']}")
                explanation = generate_bank_match_explanation(loan, user_profile)
                st.caption(explanation)

# -------------------------------------------------
# 6️⃣ IMPROVEMENT TIPS
# -------------------------------------------------
st.divider()
st.subheader("💡 Improvement Suggestions")

tips = generate_improvement_tips(user_profile, risk_level)

if tips:
    for tip in tips:
        st.markdown(f"- {tip}")
else:
    st.markdown("✔ Your profile is already strong. No immediate improvements needed.")

# -------------------------------------------------
# 7️⃣ DISCLAIMER
# -------------------------------------------------
st.divider()
st.caption(
    "⚠️ This system is a **predictive and advisory model** created for educational "
    "purposes only. It does not guarantee loan approval or access real bank data."
)
