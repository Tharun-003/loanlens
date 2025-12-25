def generate_risk_explanation(profile: dict, risk_level: str) -> str:
    reasons = []

    if profile.get("existing_loan") == "Yes":
        reasons.append("existing loan obligations")

    if profile.get("emi_delay") == "Frequent":
        reasons.append("frequent past EMI delays")
    elif profile.get("emi_delay") == "Sometimes":
        reasons.append("occasional past EMI delays")

    if profile.get("credit_score") == "Low":
        reasons.append("low credit score")
    elif profile.get("credit_score") == "Medium":
        reasons.append("moderate credit score")

    if not reasons:
        return "Your profile shows stable repayment behaviour with minimal risk indicators."

    reason_text = ", ".join(reasons)
    return f"{risk_level} risk identified due to {reason_text}."


def generate_eligibility_explanation(loan_type: str, eligibility: str) -> str:
    if eligibility == "Eligible":
        return f"Your profile satisfies the basic eligibility conditions for a {loan_type.lower()} loan."

    if eligibility == "Borderline":
        return (
            f"Your profile partially meets the eligibility criteria for a {loan_type.lower()} loan. "
            "Minor improvements could enhance approval chances."
        )

    return (
        f"Your profile does not currently meet the key eligibility requirements "
        f"for a {loan_type.lower()} loan."
    )


def generate_bank_match_explanation(loan: dict, profile: dict) -> str:
    explanations = []

    explanations.append(
        f"{loan['bank_name']} offers this loan for applicants with "
        f"{loan['credit_required'].lower()} credit score profiles."
    )

    if profile.get("coapplicant") == "Yes":
        explanations.append("Availability of a co-applicant strengthens the loan profile.")

    explanations.append(
        f"The bank's risk tolerance aligns with your current risk level."
    )

    return " ".join(explanations)


def generate_improvement_tips(profile: dict, risk_level: str) -> list:
    tips = []

    if profile.get("credit_score") in ["Low", "Medium"]:
        tips.append("Improving your credit score may enhance eligibility.")

    if profile.get("emi_delay") in ["Sometimes", "Frequent"]:
        tips.append("Maintaining consistent EMI payments can reduce risk.")

    if profile.get("existing_loan") == "Yes":
        tips.append("Reduccing existing loan burden may improve repayment capacity.")

    if risk_level == "High":
        tips.append("Lowering financial obligations could significantly reduce risk.")

    return tips
