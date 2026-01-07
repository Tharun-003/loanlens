def rule_based_eligibility(profile, risk):
    raw_loan_type = profile.get("loan_type")

    # Safe handling
    loan_type = str(raw_loan_type).capitalize() if raw_loan_type else "Unknown"

    reasons = []
    advisory_parts = []

    # High level risk-based guidance
    if risk == "Low":
        advisory_parts.append(
            "You have a low financial risk profile; you are likely eligible for favorable terms.")
        reasons.append("Low financial risk profile")
    elif risk == "Medium":
        advisory_parts.append(
            "Approval is possible but lenders may offer conservative terms. Consider improving key metrics.")
        reasons.append("Moderate financial risk profile")
    else:
        advisory_parts.append(
            "Higher financial risk detected; approval may require stronger documentation or a co-applicant.")
        reasons.append("High financial risk profile")

    # Personalized suggestions based on numeric indicators
    credit_score = int(profile.get("credit_score", 0) or 0)
    monthly_income = float(profile.get("monthly_income", 0) or 0)
    loan_amount = float(profile.get("loan_amount", 0) or 0)
    pending_amount = float(profile.get("pending_amount", 0) or 0)
    has_existing = profile.get("has_existing", "No")

    # Credit score guidance
    if credit_score < 550:
        advisory_parts.append(
            "Your credit score is low — focus on clearing delinquencies and building credit history.")
        reasons.append("Low credit score")
    elif credit_score < 650:
        advisory_parts.append(
            "Your credit score is below optimal; improving it can materially improve offers.")
        reasons.append("Below-optimal credit score")
    else:
        advisory_parts.append(
            "Credit score is reasonable; lenders will view this positively.")
        reasons.append("Good credit score")

    # Affordability signal
    if monthly_income <= 0:
        advisory_parts.append(
            "We couldn't find a stable income in your profile. Provide income documentation to improve eligibility.")
        reasons.append("Missing income information")
    else:
        # heuristic: loans larger than 5x annual income are high burden
        annual_income = monthly_income * 12
        if loan_amount > 5 * annual_income:
            advisory_parts.append(
                "Requested loan size appears large relative to income; consider lowering the amount or adding a co-applicant.")
            reasons.append("High loan-to-income ratio")
        elif loan_amount > 2 * annual_income:
            advisory_parts.append(
                "Requested loan is significant; expect stricter underwriting and possibly higher rates.")
            reasons.append("Significant loan-to-income ratio")
        else:
            advisory_parts.append(
                "Requested loan amount is within a reasonable range for your income.")
            reasons.append("Reasonable loan-to-income ratio")

    # Existing loan advice (if present)
    if has_existing == "Yes" and pending_amount > 0:
        advisory_parts.append(
            "You have an outstanding loan — consider refinancing if the recommended lender offers a lower rate.")
        reasons.append("Existing loan pending")

    # Loan-type specific notes
    if "home" in loan_type.lower():
        prop = float(profile.get("property_value", 0) or 0)
        down = float(profile.get("down_payment", 0) or 0)
        if prop > 0 and down / prop < 0.2:
            advisory_parts.append(
                "Down payment is below 20% — lenders may ask for higher margins or insurance.")
            reasons.append("Low down payment for property")
    elif "education" in loan_type.lower():
        country = profile.get("study_country", "").strip()
        if country and country.lower() != "india":
            advisory_parts.append(
                "Studying abroad can affect loan terms; ensure you provide overseas admission and sponsor details.")
            reasons.append("Overseas study funding")
    elif "personal" in loan_type.lower():
        emp = profile.get("employment_type", "").lower()
        if emp == "self-employed":
            advisory_parts.append(
                "Self-employed applicants should provide 2+ years of financial statements for better offers.")
            reasons.append("Self-employed applicant")

    # Final advisory string
    advisory = " ".join(advisory_parts)
    reasons.append(f"Loan type evaluated: {loan_type}")

    return advisory, reasons
