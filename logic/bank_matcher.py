import pandas as pd

# -----------------------------
# Helper: risk level ordering
# -----------------------------
RISK_ORDER = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

CREDIT_ORDER = {
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
    Recommend suitable bank loans based on:
    - Loan type
    - Age
    - Credit score
    - Co-applicant availability
    - User risk level

    Returns a list of recommended loan dictionaries.
    """

    # Load dataset
    df = pd.read_csv(dataset_path)

    # Normalize values (safety)
    df["loan_type"] = df["loan_type"].str.capitalize()
    df["credit_score_required"] = df["credit_score_required"].str.capitalize()
    df["risk_tolerance"] = df["risk_tolerance"].str.capitalize()

    recommendations = []

    for _, row in df.iterrows():

        # 1️⃣ Loan type must match
        if row["loan_type"] != user_profile["loan_type"]:
            continue

        # 2️⃣ Age check
        if user_profile["age"] < row["min_age"]:
            continue

        # 3️⃣ Credit score check
        if CREDIT_ORDER[user_profile["credit_score"]] < CREDIT_ORDER[row["credit_score_required"]]:
            continue

        # 4️⃣ Co-applicant check (if required)
        if row["requires_coapplicant"] == "Yes" and user_profile.get("coapplicant", "No") != "Yes":
            continue

        # 5️⃣ Risk tolerance check
        if RISK_ORDER[user_risk] > RISK_ORDER[row["risk_tolerance"]]:
            continue

        # If all checks passed → recommend
        recommendations.append({
            "bank_name": row["bank_name"],
            "loan_name": row["loan_name"],
            "loan_type": row["loan_type"],
            "risk_tolerance": row["risk_tolerance"],
            "credit_required": row["credit_score_required"]
        })

    # Limit results
    return recommendations[:top_n]
