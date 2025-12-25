def rule_based_eligibility(profile: dict, risk_level: str) -> str:
    """
    Rule-based eligibility check.
    Returns: 'Eligible', 'Borderline', or 'Not Eligible'
    """

    loan_type = profile.get("loan_type")
    age = profile.get("age")
    credit = profile.get("credit_score")
    employment = profile.get("employment_stability")
    admission = profile.get("admission_confirmed", "No")
    income = profile.get("income", 0)

    # ------------------------
    # HARD REJECTION RULES
    # ------------------------

    # Age-based rejection
    if loan_type == "Education" and age < 17:
        return "Not Eligible"

    if loan_type == "Home" and age < 21:
        return "Not Eligible"

    if loan_type == "Personal" and age < 23:
        return "Not Eligible"

    # Credit score hard stop
    if credit == "Low" and risk_level == "High":
        return "Not Eligible"

    # Home loan must have income
    if loan_type == "Home" and income <= 0:
        return "Not Eligible"

    # Education loan must have admission confirmation
    if loan_type == "Education" and admission != "Yes":
        return "Not Eligible"

    # ------------------------
    # BORDERLINE CONDITIONS
    # ------------------------

    # Medium risk always treated cautiously
    if risk_level == "Medium":
        return "Borderline"

    # Personal loan requires stable employment
    if loan_type == "Personal" and employment == "Low":
        return "Borderline"

    # Medium credit score for secured loans
    if credit == "Medium" and loan_type in ["Home", "Personal"]:
        return "Borderline"

    # ------------------------
    # ELIGIBLE
    # ------------------------

    return "Eligible"
