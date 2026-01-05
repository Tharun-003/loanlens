import os
import pandas as pd

# =========================================================
# PROJECT ROOT (FinSense/)
# =========================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================================================
# DATASET MAPPING
# =========================================================
DATASETS = {
    "Home Loan": "final_home_loan.csv",
    "Personal Loan": "final_personal_loan.csv",
    "Education Loan": "final_education_loans.csv",
}

# =========================================================
# MAX NUMBER OF SUGGESTIONS
# =========================================================
MAX_SUGGESTIONS = 3


def recommend_loans(user_profile, risk_level):
    """
    Recommend loans from CSV datasets for awareness.
    Never rejects completely – uses suitability labels instead.
    """

    loan_type = user_profile.get("loan_type")
    credit_score = int(user_profile.get("credit_score", 0))
    requested_amount = int(user_profile.get("new_loan_amount", 0))

    # -----------------------------------------------------
    # Validate loan type
    # -----------------------------------------------------
    if loan_type not in DATASETS:
        return []

    # -----------------------------------------------------
    # Resolve dataset path
    # -----------------------------------------------------
    csv_path = os.path.join(PROJECT_ROOT, DATASETS[loan_type])

    if not os.path.exists(csv_path):
        print(f"[ERROR] Dataset not found: {csv_path}")
        return []

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    df = pd.read_csv(csv_path)

    if df.empty:
        return []

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # -----------------------------------------------------
    # Helper functions
    # -----------------------------------------------------
    def pick(row, keys, default=None):
        for k in keys:
            if k in row and pd.notna(row[k]):
                return row[k]
        return default

    def to_int(val, default=0):
        try:
            return int(float(val))
        except Exception:
            return default

    # Column name flexibility
    min_credit_keys = ["min_credit", "min_credit_score", "cibil_score"]
    max_amount_keys = ["max_amount", "max_loan_amount", "loan_amount"]
    loan_name_keys = ["loan_name", "product_name"]
    bank_keys = ["bank", "bank_name", "lender"]
    interest_keys = ["interest_rate", "rate"]
    tenure_keys = ["tenure", "loan_tenure", "loan_term"]

    recommendations = []

    # -----------------------------------------------------
    # Build recommendations (AWARENESS MODE)
    # -----------------------------------------------------
    for _, row in df.iterrows():
        min_credit = to_int(pick(row, min_credit_keys), 0)
        max_amount = to_int(pick(row, max_amount_keys), 0)

        # ---- Suitability logic (NO REJECTION) ----
        if credit_score < min_credit:
            match = "Cautious"
            reason = (
                "Shown for awareness only. Eligibility may be limited "
                "due to low credit score."
            )
        else:
            if max_amount > 0 and requested_amount <= max_amount:
                match = "Excellent" if risk_level == "Low" else "Good"
            else:
                match = "Suitable"

            reason = "Matches your credit profile and planned loan amount."

        recommendations.append({
            "loan_name": pick(row, loan_name_keys, "Loan"),
            "bank": pick(row, bank_keys, "Bank"),
            "interest_rate": pick(row, interest_keys, "N/A"),
            "tenure": pick(row, tenure_keys, "N/A"),
            "max_amount": f"{max_amount:,}" if max_amount > 0 else "N/A",
            "match": match,
            "reason": reason
        })

    # -----------------------------------------------------
    # Return top N loans
    # -----------------------------------------------------
    return recommendations[:MAX_SUGGESTIONS]
