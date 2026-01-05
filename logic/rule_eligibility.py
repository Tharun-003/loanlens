def rule_based_eligibility(profile, risk):
    raw_loan_type = profile.get("loan_type")

    # ✅ SAFE handling
    if not raw_loan_type:
        loan_type = "Unknown"
    else:
        loan_type = str(raw_loan_type).capitalize()

    reasons = []
    advisory = ""

    if risk == "Low":
        advisory = "You are eligible for most loan products."
        reasons.append("Low financial risk")
    elif risk == "Medium":
        advisory = "Loan possible with cautious terms."
        reasons.append("Moderate financial risk")
    else:
        advisory = "Loan approval not recommended."
        reasons.append("High financial risk")

    reasons.append(f"Loan type evaluated: {loan_type}")

    return advisory, reasons
