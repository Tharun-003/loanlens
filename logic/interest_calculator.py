def calculate_pending_interest(principal, annual_rate, total_months, risk_level):
    # 1. Risk-Adjusted Rate Logic
    # Add a penalty for higher risk profiles
    risk_penalty = 0
    if risk_level == "Medium":
        risk_penalty = 1.5  # +1.5% interest
    elif risk_level == "High":
        risk_penalty = 3.5  # +3.5% interest

    adjusted_rate = annual_rate + risk_penalty
    
    # 2. Simple Interest Calculation for remaining period
    # Formula: I = (P * R * T) / 100
    # T is in years, so divide months by 12
    time_years = total_months / 12
    interest_amount = (principal * adjusted_rate * time_years) / 100

    return {
        "pending_interest": round(interest_amount, 2),
        "adjusted_rate": f"{adjusted_rate}%",
        "months_remaining": total_months
    }