def calculate_pending_interest(principal, annual_rate, total_months, risk_level=None):
    """
    Calculates remaining interest on an existing loan
    using risk-adjusted reducing balance logic.
    """

    # Safety checks
    if principal <= 0 or annual_rate <= 0 or total_months <= 0:
        return {
            "pending_interest": 0.0,
            "adjusted_rate": annual_rate,
            "months_remaining": total_months
        }

    # Risk penalty
    risk_penalty = 0.0
    if risk_level == "Medium":
        risk_penalty = 1.5
    elif risk_level == "High":
        risk_penalty = 3.5

    adjusted_rate = annual_rate + risk_penalty
    monthly_rate = adjusted_rate / 12 / 100

    balance = principal
    principal_payment = principal / total_months
    total_interest = 0.0

    for _ in range(total_months):
        interest = balance * monthly_rate
        total_interest += interest
        balance -= principal_payment

    return {
        "pending_interest": round(total_interest, 2),
        "adjusted_rate": round(adjusted_rate, 2),
        "months_remaining": total_months
    }
