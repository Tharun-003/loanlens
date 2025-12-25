from utils.constants import (
    CREDIT_SCORE_MAP,
    EMPLOYMENT_STABILITY_MAP,
    EMI_DELAY_MAP,
    LOAN_TYPE_MAP
)

def encode_user_profile(profile: dict) -> dict:
    return {
        "age": profile["age"],
        "income": profile["income"],
        "credit_score": CREDIT_SCORE_MAP[profile["credit_score"]],
        "employment_stability": EMPLOYMENT_STABILITY_MAP[profile["employment_stability"]],
        "existing_loan": 1 if profile["existing_loan"] == "Yes" else 0,
        "emi_delay": EMI_DELAY_MAP[profile["emi_delay"]],
        "loan_type": LOAN_TYPE_MAP[profile["loan_type"]]
    }
