import pandas as pd

# -----------------------------
# Helper: risk ordering
# -----------------------------
RISK_ORDER = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}


def recommend_loans(
    user_profile: dict,
    user_risk: str,
    dataset_path: str = "data/bank_loan_master.csv",
    top_n: int = 3
):
    """
    Suggest suitable loans strictly from dataset for awareness purposes.

    NOTE:
    - This does NOT approve or reject loans
    - This only checks dataset criteria for suitability display
    """

    df = pd.read_csv(dataset_path)

    # Normalize text columns
    df["loan_type"] = df["loan_type"].str.capitalize()
    df["risk_tolerance"] = df["risk_tolerance"].str.capitalize()

    recommendations = []

    for _, row in df.iterrows():

        # 1️⃣ Loan type match
        if row["loan_type"] != user_profile["loan_type"]:
            continue

        # 2️⃣ Age awareness check (dataset criteria)
        if user_profile["age"] < row["min_age"]:
            continue

        # 3️⃣ Credit score awareness check (NUMERIC)
        if user_profile["credit_score"] < row["min_credit_score"]:
            continue

        # 4️⃣ Income awareness check
        if user_profile["income"] < row["min_income"]:
            continue

        # 5️⃣ Risk suitability (advisory, not approval)
        if RISK_ORDER[user_risk] > RISK_ORDER[row["risk_tolerance"]]:
            suitability = "Risky"
        elif RISK_ORDER[user_risk] < RISK_ORDER[row["risk_tolerance"]]:
            suitability = "Safer"
        else:
            suitability = "Moderate"

        recommendations.append({
            "bank_name": row["bank_name"],
            "loan_name": row["loan_name"],
            "loan_type": row["loan_type"],
            "interest_rate": row["interest_rate"],
            "tenure_range": row["tenure_range"],
            "min_income": row["min_income"],
            "min_credit_score": row["min_credit_score"],
            "risk_tolerance": row["risk_tolerance"],
            "suitability": suitability,
            "explanation": (
                "This loan is shown because your details align with the dataset’s "
                "basic income and credit score criteria."
            )
        })

    return recommendations[:top_n]
