def rule_based_eligibility(profile: dict, risk_level: str):
    """
    Advisory eligibility assessment for financial awareness only.

    Returns:
        status (str): 'Recommended', 'Proceed with Caution', 'Not Advisable Currently'
        reasons (list): Simple explanations for the status
    """

    loan_type = profile.get("loan_type")
    age = profile.get("age")
    credit_score = profile.get("credit_score")
    employment = profile.get("employment_type")
    income = profile.get("income", 0)
    admission = profile.get("admission_confirmed", "No")

    reasons = []

    # ------------------------
    # Awareness-based checks
    # ------------------------

    # Age awareness
    if loan_type == "Education" and age < 17:
        reasons.append("Age is below the usual range for education loans")

    if loan_type == "Home" and age < 21:
        reasons.append("Age is on the lower side for long-term home loan repayment")

    if loan_type == "Personal" and age < 23:
        reasons.append("Personal loans usually require stable earning age")

    # Credit score awareness (numeric)
    if credit_score < 600:
        reasons.append("Credit score is currently low")
    elif credit_score < 700:
        reasons.append("Credit score is average")

    # Income awareness
    if loan_type == "Home" and income <= 0:
        reasons.append("Stable income is important for home loan repayment")

    # Education loan awareness
    if loan_type == "Education" and admission != "Yes":
        reasons.append("Loan consideration is safer after admission confirmation")

    # Employment awareness
    if loan_type == "Personal" and employment in ["Student", "Unemployed"]:
        reasons.append("Personal loans are easier with stable employment")

    # ------------------------
    # Advisory decision
    # ------------------------

    if risk_level == "High":
        status = "Not Advisable Currently"
    elif risk_level == "Medium" or reasons:
        status = "Proceed with Caution"
    else:
        status = "Recommended"

    return status, reasons
