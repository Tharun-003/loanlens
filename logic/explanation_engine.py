def generate_risk_explanation(profile: dict, risk_level: str) -> str:
    """
    Generates a simple, human-readable explanation for the user's risk level.
    """

    reasons = []

    # Existing loan awareness
    if profile.get("has_existing_loan"):
        reasons.append("you already have an existing loan")

    # Income vs expense pressure
    income = profile.get("income", 0)
    expenses = profile.get("expenses", 0)
    if income > 0:
        expense_ratio = expenses / income
        if expense_ratio > 0.6:
            reasons.append("a high portion of your income goes towards monthly expenses")
        elif expense_ratio > 0.4:
            reasons.append("a moderate portion of your income is spent on expenses")

    # Credit score awareness (numeric)
    credit_score = profile.get("credit_score", 0)
    if credit_score < 600:
        reasons.append("your credit score is currently low")
    elif credit_score < 700:
        reasons.append("your credit score is in the average range")

    # Age vs repayment horizon
    age = profile.get("age", 0)
    tenure = profile.get("tenure", 0)
    if age + tenure > 60:
        reasons.append("the repayment period extends to a later stage of life")

    if not reasons:
        return (
            "Your financial profile appears stable with balanced income, expenses, "
            "and manageable repayment capacity."
        )

    return f"Your financial risk is assessed as {risk_level} because " + ", ".join(reasons) + "."


def generate_eligibility_explanation(loan_type: str, advisory_status: str) -> str:
    """
    Explains the advisory status shown on the result page.
    """

    if advisory_status == "Recommended":
        return (
            f"Based on your current financial profile, taking a {loan_type.lower()} loan "
            "appears manageable."
        )

    if advisory_status == "Proceed with Caution":
        return (
            f"A {loan_type.lower()} loan may be possible, but some financial indicators "
            "suggest careful planning is required."
        )

    return (
        f"It may be better to postpone taking a {loan_type.lower()} loan until "
        "your financial situation improves."
    )


def generate_bank_match_explanation(loan: dict) -> str:
    """
    Explains why a particular loan from the dataset is suggested.
    """

    return (
        f"This loan from {loan['bank_name']} is suggested because it matches your selected "
        f"loan type and aligns with the basic income and credit score criteria "
        f"defined in the dataset."
    )


def generate_improvement_tips(profile: dict, risk_level: str) -> list:
    """
    Provides practical financial improvement tips.
    """

    tips = []

    # Credit score tips
    if profile.get("credit_score", 0) < 700:
        tips.append("Improving your credit score through timely payments can help.")

    # Expense management tips
    income = profile.get("income", 0)
    expenses = profile.get("expenses", 0)
    if income > 0 and expenses / income > 0.5:
        tips.append("Reducing unnecessary monthly expenses can improve repayment comfort.")

    # Existing loan tips
    if profile.get("has_existing_loan"):
        tips.append("Reducing or closing existing loan obligations may help before taking a new loan.")

    # High-risk warning
    if risk_level == "High":
        tips.append("Avoid taking new loans until your financial stability improves.")

    return tips
