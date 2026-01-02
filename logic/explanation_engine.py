def generate_risk_explanation(profile: dict, risk_level: str) -> str:
    """
    Generates a human-readable explanation matching the trained model's features.
    """
    reasons = []

    # 1. CIBIL (Credit Score) - Aligned with your training data
    cibil = profile.get("cibil_score", 0)
    if cibil < 500:
        reasons.append("your credit score is significantly below the preferred banking threshold")
    elif cibil < 700:
        reasons.append("your credit score is in the average range, which increases risk")

    # 2. Income vs. Loan Pressure (Debt-to-Income)
    income = profile.get("income_annum", 0)
    loan_amt = profile.get("loan_amount", 0)
    
    if income > 0:
        # Check if the requested loan is more than 3x the annual income
        if (loan_amt / income) > 3:
            reasons.append("the requested loan amount is very high relative to your annual income")

    # 3. Assets vs. Loan (Collateral awareness)
    # This matches the features the Decision Tree uses to split nodes
    assets = (profile.get("residential_assets_value", 0) + 
              profile.get("commercial_assets_value", 0))
    if assets < loan_amt:
        reasons.append("your total asset value is lower than the loan amount requested")

    if not reasons:
        return (
            "Your financial profile appears stable based on our model's criteria, "
            "showing a healthy balance between income, assets, and credit history."
        )

    return f"Your financial risk is assessed as {risk_level} because " + ", ".join(reasons) + "."


def generate_improvement_tips(profile: dict, risk_level: str) -> list:
    """
    Provides tips based on the 80% accuracy model's common rejection reasons.
    """
    tips = []

    # Credit score improvement
    if profile.get("cibil_score", 0) < 700:
        tips.append("Focus on making all current utility and credit payments on time to boost your CIBIL score.")

    # Loan-to-Income adjustment
    income = profile.get("income_annum", 0)
    loan_amt = profile.get("loan_amount", 0)
    if income > 0 and (loan_amt / income) > 2:
        tips.append("Consider applying for a smaller loan amount to lower your debt-to-income ratio.")

    # High-risk specific advice
    if risk_level == "High":
        tips.append("We recommend waiting 6 months while building up your savings before reapplying.")

    return tips