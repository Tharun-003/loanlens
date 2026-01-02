import pandas as pd

# -----------------------------
# Helper: risk ordering for advisory logic
# -----------------------------
RISK_ORDER = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

def recommend_loans(
    user_profile: dict,
    user_risk: str,
    dataset_path: str = "../data/bank_loan_master.csv",
    top_n: int = 3
):
    """
    Suggests suitable bank products by matching user profiles against bank criteria.
    """
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        return []

    # Normalize text columns for accurate matching
    df["loan_type"] = df["loan_type"].str.capitalize()
    df["risk_tolerance"] = df["risk_tolerance"].str.capitalize()

    recommendations = []

    # Get user values using the specific keys used in training
    u_income = user_profile.get("income_annum", 0)
    u_cibil = user_profile.get("cibil_score", 0)
    u_loan_type = user_profile.get("loan_type", "").capitalize()

    for _, row in df.iterrows():

        # 1️⃣ Loan type match
        if row["loan_type"] != u_loan_type:
            continue

        # 2️⃣ Credit score awareness check (Matching CIBIL standards)
        if u_cibil < row["min_credit_score"]:
            continue

        # 3️⃣ Income awareness check (Matching Annual Income)
        if u_income < row["min_income"]:
            continue

        # 4️⃣ Risk suitability advisory
        # Compares model-predicted risk against the bank's risk tolerance
        u_risk_val = RISK_ORDER.get(user_risk, 3)
        b_risk_val = RISK_ORDER.get(row["risk_tolerance"], 2)

        if u_risk_val > b_risk_val:
            suitability = "Risky"
        elif u_risk_val < b_risk_val:
            suitability = "Safer"
        else:
            suitability = "Moderate"

        recommendations.append({
            "bank_name": row["bank_name"],
            "loan_name": row["loan_name"],
            "interest_rate": row["interest_rate"],
            "suitability": suitability,
            "explanation": (
                f"Matched with {row['bank_name']} based on your income and "
                f"CIBIL score of {u_cibil}."
            )
        })

    # Sort by interest rate (lowest first) before returning top N
    recommendations = sorted(recommendations, key=lambda x: x['interest_rate'])
    
    return recommendations[:top_n]