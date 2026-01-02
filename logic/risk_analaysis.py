def calculate_risk(user_profile: dict):
    """
    Determines the user's financial risk level based on
    income, expenses, credit score, existing loan burden,
    age, and repayment horizon.

    Returns:
        risk_level (str): Low / Medium / High
        explanation (str): Simple human-readable explanation
    """

    income = user_profile["income"]
    expenses = user_profile["expenses"]
    credit_score = user_profile["credit_score"]
    age = user_profile["age"]
    tenure = user_profile["tenure"]
    has_existing_loan = user_profile.get("has_existing_loan", False)

    # -----------------------------
    # Core calculations
    # -----------------------------
    expense_ratio = expenses / income
    risk_score = 0
    reasons = []

    # Expense vs income analysis
    if expense_ratio > 0.6:
        risk_score += 2
        reasons.append("A large portion of income is spent on monthly expenses")
    elif expense_ratio > 0.4:
        risk_score += 1
        reasons.append("Moderate portion of income goes towards expenses")

    # Credit score awareness
    if credit_score < 600:
        risk_score += 2
        reasons.append("Credit score is on the lower side")
    elif credit_score < 700:
        risk_score += 1
        reasons.append("Credit score is average")

    # Existing loan burden
    if has_existing_loan:
        risk_score += 1
        reasons.append("Existing loan increases financial responsibility")

    # Age vs repayment horizon
    if age + tenure > 60:
        risk_score += 1
        reasons.append("Repayment period extends to a later stage of life")

    # -----------------------------
    # Risk classification
    # -----------------------------
    if risk_score <= 1:
        risk_level = "Low"
    elif risk_score <= 3:
        risk_level = "Medium"
    else:
        risk_level = "High"

    explanation = (
        f"Your financial risk is assessed as {risk_level} because "
        + ", ".join(reasons)
        + "."
        if reasons else
        "Your financial indicators are balanced with manageable repayment capacity."
    )

    return risk_level, explanation
