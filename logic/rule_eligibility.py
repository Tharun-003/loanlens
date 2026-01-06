def rule_based_eligibility(profile, risk):
    raw_loan_type = profile.get("loan_type")

    # Safe handling
    loan_type = str(raw_loan_type).capitalize() if raw_loan_type else "Unknown"

    reasons = []
    advisory = ""

    if risk == "Low":
        advisory = "You are financially stable and eligible for most loan products."
        reasons.append("Low financial risk profile")

    elif risk == "Medium":
        advisory = "Loan approval is possible, but terms may be cautious."
        reasons.append("Moderate financial risk profile")

    else:
        advisory = "Higher financial risk detected. Approval depends on lender discretion."
        reasons.append("High financial risk profile")

    # Informational only
    reasons.append(f"Loan type evaluated: {loan_type}")

    return advisory, reasons
