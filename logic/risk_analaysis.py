def calculate_risk(user_profile: dict):
    """
    Determines the user's financial risk level using features aligned with the 
    trained Decision Tree model.
    """

    # 1. Standardize variable names to match training data
    income = user_profile.get("income_annum", 0)
    loan_amount = user_profile.get("loan_amount", 0)
    cibil_score = user_profile.get("cibil_score", 0)
    # Using 'loan_term' which usually correlates with repayment horizon
    tenure = user_profile.get("loan_term", 0) 
    
    # Calculate assets value as a risk mitigator
    assets = (user_profile.get("residential_assets_value", 0) + 
              user_profile.get("commercial_assets_value", 0))

    risk_score = 0
    reasons = []

    # 2. Debt-to-Income (DTI) Analysis
    # In banking, if a loan is > 3x annual income, it is high risk
    if income > 0:
        dti_ratio = loan_amount / income
        if dti_ratio > 4:
            risk_score += 3
            reasons.append("the loan amount is more than 4x your annual income")
        elif dti_ratio > 2.5:
            risk_score += 1
            reasons.append("the loan-to-income ratio is moderately high")

    # 3. CIBIL (Credit Score) Awareness
    if cibil_score < 400:
        risk_score += 3
        reasons.append("your CIBIL score is critically low")
    elif cibil_score < 650:
        risk_score += 1
        reasons.append("your credit score is in the average range")

    # 4. Asset Coverage Awareness
    # Matches the 'assets' feature often used by Decision Trees
    if assets < (loan_amount * 0.5):
        risk_score += 1
        reasons.append("your total asset value provides low coverage for the loan")

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
        "Your financial indicators are balanced with a healthy CIBIL score and manageable debt."
    )

    return risk_level, explanation