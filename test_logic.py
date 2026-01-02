from logic.risk_analaysis import calculate_risk
from logic.interest_calculator import calculate_pending_interest
from logic.loan_recommender import recommend_loans
from logic.explanation_engine import (
    generate_risk_explanation,
    generate_eligibility_explanation,
    generate_improvement_tips
)

# Sample user input
user_profile = {
    "loan_type": "Home",
    "age": 25,
    "income": 50000,
    "expenses": 20000,
    "credit_score": 680,
    "tenure": 20,
    "has_existing_loan": True
}

# 1️⃣ Risk analysis
risk_level, risk_explanation = calculate_risk(user_profile)
print("Risk Level:", risk_level)
print("Risk Explanation:", risk_explanation)

# 2️⃣ Pending interest check
pending_interest = calculate_pending_interest(
    pending_amount=300000,
    interest_rate=9.0,
    remaining_years=5
)


print("Pending Interest:", pending_interest)

# 3️⃣ Loan recommendation
loans = recommend_loans(user_profile, risk_level)
print("Recommended Loans:", loans)

# 4️⃣ Improvement tips
tips = generate_improvement_tips(user_profile, risk_level)
print("Tips:", tips)
