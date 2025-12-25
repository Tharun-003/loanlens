# Categorical encodings
CREDIT_SCORE_MAP = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

EMPLOYMENT_STABILITY_MAP = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

EMI_DELAY_MAP = {
    "Never": 0,
    "Sometimes": 1,
    "Frequent": 2
}

LOAN_TYPE_MAP = {
    "Education": 0,
    "Home": 1,
    "Personal": 2
}

# Reverse maps (optional)
REVERSE_LOAN_TYPE_MAP = {v: k for k, v in LOAN_TYPE_MAP.items()}
