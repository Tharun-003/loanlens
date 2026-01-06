import os
import pickle
import pandas as pd
import random

# ---------------- PROJECT ROOT ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- MODELS ----------------
MODELS = {
    "Education Loan": ("education_model.pkl", "education"),
    "Home Loan": ("home_model.pkl", "home"),
    "Personal Loan": ("personal_model.pkl", "personal"),
}

# ---------------- BANK MAPPING ----------------
BANK_MAPPING = {
    "Education Loan": ["SBI", "HDFC", "ICICI"],
    "Home Loan": ["HDFC", "ICICI", "SBI"],
    "Personal Loan": ["HDFC", "ICICI", "Axis Bank"],
}


# ---------------- LOAD ENCODER ----------------
def load_encoder(prefix, col):
    path = os.path.join(PROJECT_ROOT, "models", f"{prefix}_{col}_encoder.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


# ---------------- LOAN RECOMMENDER ----------------
def recommend_loans(user_profile, risk_level):
    """
    Dataset-aligned loan recommendation
    ✔ Uses only user-selected loan type
    ✔ Ranks instead of rejecting
    ✔ Returns Top 5 (or fewer if limited)
    """

    selected_loan_type = user_profile.get("loan_type")
    results = []

    for loan_name, (model_file, prefix) in MODELS.items():

        # ✅ CRITICAL FIX: FILTER BY USER SELECTION
        if selected_loan_type and loan_name != selected_loan_type:
            continue

        # -------- Load trained model --------
        model_path = os.path.join(PROJECT_ROOT, "models", model_file)
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        # -------- Build ML input row --------
        row = {}

        for col in model.feature_names_in_:

            if col == "age":
                row[col] = user_profile.get("age", 30)

            elif col == "credit_score":
                row[col] = user_profile.get("credit_score", 650)

            elif col == "monthly_income":
                row[col] = user_profile.get("monthly_income", 30000)

            elif col == "loan_amount":
                row[col] = user_profile.get("loan_amount", 0)

            elif col == "loan_tenure":
                row[col] = user_profile.get("loan_tenure", 10)

            elif col == "property_value":
                row[col] = user_profile.get("property_value", 0)

            elif col == "down_payment":
                row[col] = user_profile.get("down_payment", 0)

            else:
                encoder = load_encoder(prefix, col)
                if encoder:
                    value = str(user_profile.get(col, encoder.classes_[0]))
                    if value not in encoder.classes_:
                        value = encoder.classes_[0]
                    row[col] = encoder.transform([value])[0]
                else:
                    row[col] = 0

        X = pd.DataFrame([row], columns=model.feature_names_in_)

        # -------- ML Prediction --------
        approval_prob = model.predict_proba(X)[0][1]

        # -------- Eligibility Logic --------
        requested = user_profile.get("loan_amount", 0)

        if loan_name == "Home Loan":
            eligible = int(requested * 0.9)
        elif loan_name == "Education Loan":
            eligible = int(requested * 0.85)
        else:
            eligible = int(requested * 0.6)

        eligibility_ratio = eligible / requested if requested > 0 else 0

        # -------- Risk Awareness --------
        risk_bonus = 10 if risk_level == "Low" else 5 if risk_level == "Medium" else 0

        # -------- FINAL SCORE (DATASET-DRIVEN) --------
        final_score = (
            approval_prob * 70 +
            eligibility_ratio * 20 +
            risk_bonus
        )

        # -------- Recommendation Label --------
        if approval_prob >= 0.6:
            label = "Recommended"
        elif approval_prob >= 0.4:
            label = "Risky but Possible"
        else:
            label = "Not Ideal – Improve Profile"

        # -------- Bank --------
        bank = random.choice(BANK_MAPPING.get(loan_name, ["Multiple Banks"]))

        results.append({
            "loan_name": loan_name,
            "bank": bank,
            "eligible_amount": f"{eligible:,}",
            "approval_probability": round(approval_prob, 2),
            "score": int(final_score),
            "recommendation": label,
            "reason": "Based on approval trends from historical loan dataset"
        })

    # -------- SORT & RETURN --------
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]
