def encode_user_profile(user):
    """
    Convert user financial profile into numeric features.
    Aligned with CSV columns: income_annum, cibil_score, etc.
    """

    # 1. Map 'Self-employed' status as found in your training data
    # In your CSV, this is likely a binary 0/1 or "Yes"/"No" string
    is_self_employed = 1 if user.get("employment") == "Self-employed" else 0

    # 2. Loan Type mapping aligned with alphabetical LabelEncoding
    loan_type_map = {
        "Education": 0,
        "Home": 1,
        "Personal": 2
    }

    # 3. Education mapping (Graduate vs Not Graduate)
    education_map = {
        "Graduate": 1,
        "Not Graduate": 0
    }

    # Returning a dictionary that matches your model's expected feature names
    return {
        "no_of_dependents": int(user.get("dependents", 0)),
        "education": education_map.get(user.get("education_level", "Graduate"), 1),
        "self_employed": is_self_employed,
        "income_annum": int(user.get("income", 0)),
        "loan_amount": int(user.get("loan_amount", 0)),
        "loan_term": int(user.get("tenure", 0)),
        "cibil_score": int(user.get("credit_score", 0)),
        "residential_assets_value": int(user.get("res_assets", 0)),
        "commercial_assets_value": int(user.get("comm_assets", 0)),
        "luxury_assets_value": int(user.get("lux_assets", 0)),
        "bank_asset_value": int(user.get("bank_assets", 0)),
        "loan_type_encoded": loan_type_map.get(user.get("loan_type", "Personal"), 2)
    }