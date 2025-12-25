def calculate_risk(profile: dict) -> str:
    """
    Rule-based risk analysis.
    Returns: 'Low', 'Medium', or 'High'
    """

    risk_score = 0

    # Existing loan increases burden
    if profile.get("existing_loan") == "Yes":
        risk_score += 2

    # EMI payment behaviour
    if profile.get("emi_delay") == "Sometimes":
        risk_score += 2
    elif profile.get("emi_delay") == "Frequent":
        risk_score += 4

    # Credit score impact
    if profile.get("credit_score") == "Low":
        risk_score += 3
    elif profile.get("credit_score") == "Medium":
        risk_score += 1

    # Loan type base risk
    if profile.get("loan_type") == "Personal":
        risk_score += 1
    elif profile.get("loan_type") == "Home":
        risk_score += 0
    elif profile.get("loan_type") == "Education":
        risk_score -= 1  # future earning potential

    # Safety clamp
    if risk_score < 0:
        risk_score = 0

    # Map score to risk level
    if risk_score >= 6:
        return "High"
    elif risk_score >= 3:
        return "Medium"
    else:
        return "Low"
