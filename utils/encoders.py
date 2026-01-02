def encode_user_profile(user):
    """
    Convert user financial profile into numeric features
    for AI-style analysis (NOT loan approval)
    """

    employment_map = {
        "Student": 0,
        "Salaried": 1,
        "Self-employed": 2
    }

    loan_type_map = {
        "Education Loan": 0,
        "Home Loan": 1,
        "Personal Loan": 2
    }

    return {
        "age": int(user.get("age", 0)),
        "monthly_income": int(user.get("income", 0)),
        "monthly_expenses": int(user.get("expenses", 0)),
        "credit_score": int(user.get("credit_score", 0)),
        "loan_amount": int(user.get("loan_amount", 0)),
        "loan_tenure": int(user.get("tenure", 0)),
        "has_existing_loan": 1 if user.get("existing_loan") else 0,
        "employment_type": employment_map.get(
            user.get("employment", "Salaried"), 1
        ),
        "loan_type": loan_type_map.get(
            user.get("loan_type", "Personal Loan"), 2
        )
    }
