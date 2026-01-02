# -----------------------------
# Categorical Encodings (Manual for logic, but verified with model)
# -----------------------------

# Numeric Credit Score levels for rule-based calculations
CREDIT_SCORE_MAP = {
    "Poor": 0,      # Below 500
    "Average": 1,   # 500 - 700
    "Good": 2       # 700+
}

# Matches the alphabetical encoding used in clean_and_save_encoders
LOAN_TYPE_MAP = {
    "Education": 0,
    "Home": 1,
    "Personal": 2
}

# Employment types as found in many loan datasets
EMPLOYMENT_TYPE_MAP = {
    "Salaried": 0,
    "Self-Employed": 1,
    "Unemployed": 2
}

# Mapping delay history for risk assessment
EMI_DELAY_MAP = {
    "Never": 0,
    "Sometimes": 1,
    "Frequent": 2
}

# Reverse maps for UI display
REVERSE_LOAN_TYPE_MAP = {v: k for k, v in LOAN_TYPE_MAP.items()}