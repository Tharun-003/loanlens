def calculate_pending_interest(pending_amount, interest_rate, remaining_years):
    """
    Calculates approximate pending interest using simple interest.
    """
    interest = (pending_amount * interest_rate * remaining_years) / 100
    return round(interest, 2)
