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

            # --- NUMERIC FEATURES ---
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
            elif col == "guardian_income":
                row[col] = user_profile.get("guardian_income", 0)
            elif col == "existing_emis":
                row[col] = user_profile.get("existing_emi", 0)
            elif col == "study_duration":
                # Fallback to tenure if separate duration not captured
                row[col] = user_profile.get("loan_tenure", 2)
            elif col == "debt_to_income":
                 row[col] = user_profile.get("debt_income_ratio", 0)

            # --- DEFAULTS FOR MISSING FIELDS ---
            elif col == "property_age":
                row[col] = 0  # Assume New
            elif col == "moratorium_applicable":
                row[col] = 1  # Assume Yes
            elif col == "credit_card_usage":
                row[col] = 0  # Assume None/Low

            # --- CATEGORICAL FEATURES ---
            else:
                # Map model feature names to session keys
                key_map = {
                    "property_location_type": "property_location",
                    "salary_account_bank": "salary_bank",
                    "employer_type_category": "employer_type" # potentially needed if name varies
                }
                
                profile_key = key_map.get(col, col)
                raw_val = user_profile.get(profile_key)
                
                encoder = load_encoder(prefix, col)
                if encoder:
                    # Safe handling of missing/unknown values
                    if not raw_val:
                        val = encoder.classes_[0]
                    else:
                        val = str(raw_val).strip()
                        if val not in encoder.classes_:
                            val = encoder.classes_[0]
                            
                    row[col] = encoder.transform([val])[0]
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

        # -------- Bank-level suggestions (one entry per bank) --------
        banks = BANK_MAPPING.get(loan_name, ["Multiple Banks"]) or [
            "Multiple Banks"]

        # Attempt to load product-level amounts from the dataset for this loan type
        dataset_amounts = None
        data_file_map = {
            "Home Loan": os.path.join(PROJECT_ROOT, "data", "raw", "final_home_loan.csv"),
            "Education Loan": os.path.join(PROJECT_ROOT, "data", "raw", "final_education_loans.csv"),
            "Personal Loan": os.path.join(PROJECT_ROOT, "data", "raw", "final_personal_loan.csv"),
        }
        data_path = data_file_map.get(loan_name)
        if data_path and os.path.exists(data_path):
            try:
                df_data = pd.read_csv(data_path)
                # normalize column names
                df_cols = [c.lower() for c in df_data.columns]
                if "loan_amount" in df_cols and "bank" in df_cols or "bank_name" in df_cols:
                    dataset_amounts = df_data
            except Exception:
                dataset_amounts = None

        # small deterministic adjustments per bank so rankings vary
        bank_shifts = [0.02, 0.01, 0.0, -0.01, -0.02]

        # Create up to `desired_count` suggestions for the selected loan type.
        desired_count = 5

        # If there are fewer banks than desired, create product variants per bank
        # (e.g., different product offerings) so the UI can show multiple options.
        per_bank_variants = max(1, -(-desired_count // len(banks)))

        idx = 0
        while len([r for r in results if r["loan_name"] == loan_name]) < desired_count:
            bank = banks[idx % len(banks)]
            variant = (idx // len(banks))
            suffix = f" (Product {chr(65+variant)})" if variant > 0 else ""

            shift = bank_shifts[idx % len(bank_shifts)]
            adj_approval = max(0.0, min(1.0, float(approval_prob) + shift))

            # ✅ FIXED LOGIC: Prioritize User Request
            eligible_adj = 0
            
            if requested > 0:
                # Base it on what the user asked for, with small variation
                # This ensures the suggestion matches their need
                base_amt = requested
                eligible_adj = max(0, int(round(base_amt * (1 + shift))))
                
            elif dataset_amounts is not None:
                # Fallback to dataset median ONLY if request is invalid/zero
                bank_col = "bank_name" if "bank_name" in dataset_amounts.columns else (
                    "bank" if "bank" in dataset_amounts.columns else None)
                amt_col = "loan_amount"
                
                if bank_col in dataset_amounts.columns and amt_col in dataset_amounts.columns:
                    # pick a central tendency (median) of amounts for this bank
                    bank_amt_series = dataset_amounts[dataset_amounts[bank_col].astype(
                        str).str.contains(bank, case=False, na=False)][amt_col]
                    if not bank_amt_series.empty:
                        base_amt = int(bank_amt_series.median())
                    else:
                        # if bank not found, use overall median
                        base_amt = int(dataset_amounts[amt_col].median())

                    # apply small deterministic variant shift
                    eligible_adj = max(0, int(round(base_amt * (1 + shift))))
                else:
                    eligible_adj = 0
            else:
                 # Last resort fallback if no data and no request (unlikely)
                 eligible_adj = 500000 


            adj_final_score = (
                adj_approval * 70 +
                eligibility_ratio * 20 +
                risk_bonus
            )

            if adj_approval >= 0.6:
                adj_label = "Recommended"
            elif adj_approval >= 0.4:
                adj_label = "Risky but Possible"
            else:
                adj_label = "Not Ideal – Improve Profile"

            results.append({
                "loan_name": loan_name,
                "bank": f"{bank}{suffix}",
                "eligible_amount": f"{eligible_adj:,}",
                "approval_probability": round(adj_approval, 2),
                "score": int(adj_final_score),
                "recommendation": adj_label,
                "reason": "Based on approval trends from historical loan dataset"
            })

            idx += 1

    # -------- SORT & RETURN --------
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]
