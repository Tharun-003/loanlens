def rule_based_eligibility(profile: dict, risk_level: str):
    """
    Advisory eligibility assessment based on dataset-specific features.

    Returns:
        status (str): 'Recommended', 'Proceed with Caution', 'Not Advisable Currently'
        reasons (list): Simple explanations for the status
    """

    # 1. Standardize variables to match your CSV columns
    loan_type = profile.get("loan_type", "").capitalize()
    cibil_score = profile.get("cibil_score", 0)
    income = profile.get("income_annum", 0)
    is_self_employed = profile.get("self_employed", "No")
    education = profile.get("education", "Graduate")
    
    reasons = []

    # 2. CIBIL Score Awareness (Primary banking rule)
    if cibil_score < 400:
        reasons.append("CIBIL score is critically low for traditional lending standards")
    elif cibil_score < 650:
        reasons.append("CIBIL score is in the average range, which may limit options")

    # 3. Income Awareness
    if income < 200000:
        reasons.append("Annual income is below the standard stability threshold")

    # 4. Loan-Specific Awareness
    if loan_type == "Home":
        # Home loans are harder for self-employed individuals in many models
        if is_self_employed == "Yes" and cibil_score < 700:
            reasons.append("Home loans for self-employed individuals require a higher CIBIL score")
    
    if loan_type == "Education":
        # Education loans focus on future potential (Education level)
        if education == "Not Graduate":
            reasons.append("Education loans are generally prioritized for graduate-level studies")

    # 5. Asset Awareness (Safety check)
    total_assets = (profile.get("residential_assets_value", 0) + 
                    profile.get("commercial_assets_value", 0) +
                    profile.get("luxury_assets_value", 0))
    
    if total_assets == 0 and loan_type != "Personal":
        reasons.append("Absence of recorded assets increases the risk of the loan")

    # ------------------------
    # Advisory decision
    # ------------------------
    # High risk from the 80% model or critical reasons leads to 'Not Advisable'
    if risk_level == "High" or cibil_score < 350:
        status = "Not Advisable Currently"
    # Medium risk or any red flags leads to 'Proceed with Caution'
    elif risk_level == "Medium" or len(reasons) > 1:
        status = "Proceed with Caution"
    else:
        status = "Recommended"

    return status, reasons