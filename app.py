from flask import Flask, render_template, request, redirect, url_for, session

# ✅ IMPORT LOGIC
from logic.loan_recommender import recommend_loans
from logic.risk_analaysis import calculate_risk
from logic.interest_calculator import calculate_pending_interest
from logic.rule_eligibility import rule_based_eligibility


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "finsense_secret_key"


# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") and request.form.get("password"):
            session["user"] = request.form["username"]
            return redirect(url_for("home"))
    return render_template("login.html")


# -------------------------------------------------
# HOME
# -------------------------------------------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


# -------------------------------------------------
# PERSONAL DETAILS
# -------------------------------------------------
@app.route("/personal-details", methods=["GET", "POST"])
def personal_details():
    if request.method == "POST":
        session["age"] = int(request.form.get("age", 0))
        session["monthly_income"] = int(request.form.get("monthly_income", 0))
        session["credit_score"] = int(request.form.get("credit_score", 0))
        return redirect(url_for("loan_purpose"))
    return render_template("personal_details.html")


# -------------------------------------------------
# LOAN PURPOSE
# -------------------------------------------------
@app.route("/loan-purpose", methods=["GET", "POST"])
def loan_purpose():
    if request.method == "POST":
        session["loan_type"] = request.form.get("loan_type")
        return redirect(
            url_for(
                "education_loan" if session["loan_type"] == "Education"
                else "home_loan" if session["loan_type"] == "Home"
                else "personal_loan"
            )
        )
    return render_template("loan_purpose.html")


# -------------------------------------------------
# EDUCATION LOAN
# -------------------------------------------------
@app.route("/education-loan", methods=["GET", "POST"])
def education_loan():
    # Ensure the selected loan type is recorded in session (user may reach here via GET)
    session["loan_type"] = "Education"

    if request.method == "POST":
        session["loan_amount"] = int(request.form.get("loan_amount", 0))
        session["loan_tenure"] = int(request.form.get("tenure", 1))
        session["study_country"] = request.form.get("study_country")
        
        # ✅ CAPTURE MISSING FIELDS
        session["course_level"] = request.form.get("course_level")
        session["course_type"] = request.form.get("course_type")
        session["college_tier"] = request.form.get("college_tier")
        session["guardian_income"] = int(request.form.get("guardian_income", 0))
        
        return redirect(url_for("existing_loan"))
    return render_template("education_loan.html")


# -------------------------------------------------
# HOME LOAN
# -------------------------------------------------
@app.route("/home-loan", methods=["GET", "POST"])
def home_loan():
    # Ensure the selected loan type is recorded in session (user may reach here via GET)
    session["loan_type"] = "Home"

    if request.method == "POST":
        session["loan_amount"] = int(request.form.get("loan_amount", 0))
        session["loan_tenure"] = int(request.form.get("loan_tenure", 1))
        session["property_value"] = int(request.form.get("property_value", 0))
        session["down_payment"] = int(request.form.get("down_payment", 0))
        
        # ✅ CAPTURE MISSING FIELDS
        session["employment_type"] = request.form.get("employment_type")
        session["property_location"] = request.form.get("property_location")
        session["existing_emi"] = int(request.form.get("existing_emi") or 0)
        
        return redirect(url_for("existing_loan"))
    return render_template("home_loan.html")


# -------------------------------------------------
# PERSONAL LOAN
# -------------------------------------------------
@app.route("/personal-loan", methods=["GET", "POST"])
def personal_loan():
    # Ensure the selected loan type is recorded in session (user may reach here via GET)
    session["loan_type"] = "Personal"

    if request.method == "POST":
        session["loan_amount"] = int(request.form.get("loan_amount", 0))
        session["loan_tenure"] = int(request.form.get("loan_tenure", 1))
        session["employment_type"] = request.form.get("employment_type")
        
        # ✅ CAPTURE MISSING FIELDS
        session["employer_type"] = request.form.get("employer_type")
        session["salary_bank"] = request.form.get("salary_bank")
        session["debt_income_ratio"] = int(request.form.get("debt_income_ratio", 0))
        session["job_stability"] = request.form.get("job_stability")
        
        return redirect(url_for("existing_loan"))
    return render_template("personal_loan.html")


# -------------------------------------------------
# EXISTING LOAN
# -------------------------------------------------
@app.route("/existing-loan", methods=["GET", "POST"])
def existing_loan():
    if request.method == "POST":
        session["has_existing"] = request.form.get("has_existing_loan", "No")
        if session["has_existing"] == "Yes":
            return redirect(url_for("old_loan_details"))
        return redirect(url_for("result"))
    return render_template("existing_loan_check.html")


# -------------------------------------------------
# OLD LOAN DETAILS
# -------------------------------------------------
@app.route("/old-loan-details", methods=["GET", "POST"])
def old_loan_details():
    if request.method == "POST":
        session["pending_amount"] = int(request.form.get("pending_amount", 0))
        session["old_interest"] = float(request.form.get("interest_rate", 0))
        session["pending_years"] = int(request.form.get("pending_years", 1))
        return redirect(url_for("result"))
    return render_template("old_loan_details.html")


# -------------------------------------------------
# 🔥 RESULT — FINAL & DATASET-DRIVEN
# -------------------------------------------------
@app.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("login"))

    # ---------------- USER PROFILE (CRITICAL) ----------------
    user_profile = {
        "age": session.get("age", 0),
        "credit_score": session.get("credit_score", 0),
        "monthly_income": session.get("monthly_income", 0),
        "loan_amount": session.get("loan_amount", 0),
        "pending_amount": session.get("pending_amount", 0),
        "loan_tenure": session.get("loan_tenure", 1),
        "property_value": session.get("property_value", 0),
        "down_payment": session.get("down_payment", 0),
        "study_country": session.get("study_country", ""),
        "employment_type": session.get("employment_type", ""),
        "has_existing": session.get("has_existing", "No"),
        # ✅ EXPANDED FIELDS FOR ML MODELS
        "course_level": session.get("course_level"),
        "course_type": session.get("course_type"),
        "college_tier": session.get("college_tier"),
        "guardian_income": session.get("guardian_income", 0),
        "property_location": session.get("property_location"),
        "existing_emi": session.get("existing_emi", 0),
        "employer_type": session.get("employer_type"),
        "salary_bank": session.get("salary_bank"),
        "debt_income_ratio": session.get("debt_income_ratio", 0),
        "job_stability": session.get("job_stability"),
        
        # ✅ REQUIRED FOR MODEL FILTERING
        "loan_type": f"{session.get('loan_type')} Loan"
    }

    # ---------------- RISK ----------------
    risk_label, risk_score = calculate_risk(user_profile)
    risk = (
        "Low" if "low" in risk_label.lower()
        else "Medium" if "medium" in risk_label.lower()
        else "High"
    )

    # ---------------- RULES ----------------
    advisory, rule_reasons = rule_based_eligibility(user_profile, risk)

    # ---------------- ML LOAN RECOMMENDATION ----------------
    loans = recommend_loans(user_profile, risk)
    best_loan = loans[0] if loans else None
    top_loans = loans[:4]

    # ---------------- INTEREST CALCULATIONS ----------------
    pending_amount = session.get("pending_amount", 0)

    # New loan interest — compute using amortizing (reducing-balance) logic
    # Use the recommended bank's typical rate when available so comparison is realistic
    new_interest = 0.0
    chosen_new_rate = 8.0
    if best_loan and best_loan.get("bank"):
        bank_name = best_loan.get("bank").split(" (")[0]
        bank_rates = {"HDFC": 7.0, "ICICI": 7.25, "SBI": 6.9, "Axis Bank": 7.5}
        chosen_new_rate = bank_rates.get(bank_name, 8.0)

    if user_profile.get("loan_amount", 0) > 0 and user_profile.get("loan_tenure", 0) > 0:
        new_interest_data = calculate_pending_interest(
            principal=user_profile["loan_amount"],
            annual_rate=chosen_new_rate,
            total_months=max(1, int(user_profile.get("loan_tenure", 1)) * 12),
            risk_level=risk
        )

        new_interest = (
            new_interest_data.get("pending_interest", 0)
            if isinstance(new_interest_data, dict)
            else float(new_interest_data)
        )

    existing_interest = 0
    savings_percent = 0
    refinance_interest = 0

    if session.get("has_existing") == "Yes" and pending_amount > 0:
        interest_data = calculate_pending_interest(
            principal=pending_amount,
            annual_rate=session.get("old_interest", 0),
            total_months=max(1, int(session.get("pending_years", 1)) * 12),
            risk_level=risk
        )

        # Handle dict OR number safely
        existing_interest = (
            interest_data.get("pending_interest", 0)
            if isinstance(interest_data, dict)
            else float(interest_data)
        )

        # Compute refinancing cost for the pending amount using chosen_new_rate
        refinance_data = calculate_pending_interest(
            principal=pending_amount,
            annual_rate=chosen_new_rate,
            total_months=max(1, int(session.get("pending_years", 1)) * 12),
            risk_level=risk
        )
        refinance_interest = (
            refinance_data.get("pending_interest", 0)
            if isinstance(refinance_data, dict)
            else float(refinance_data)
        )

        if existing_interest > 0:
            savings_percent = round(
                ((existing_interest - refinance_interest) / existing_interest) * 100, 2
            )
    else:
        # No existing loan — compare requested new loan to zero
        if new_interest > 0:
            savings_percent = 0

    # ---------------- INTEREST SERIES FOR CHART ----------------
    loan_years = max(1, int(user_profile.get("loan_tenure", 1)))
    pending_years = int(session.get("pending_years", 1)) if session.get(
        "has_existing") == "Yes" else 0

    # If user has an existing loan, show comparison over pending_years; otherwise use loan_years
    span_years = max(
        loan_years, pending_years if pending_years > 0 else loan_years)
    interest_years = list(range(1, span_years + 1))

    # Decide principal/timebase for the 'new' series used in the chart: when refinancing,
    # use the pending_amount and pending_years so comparison is apples-to-apples.
    if session.get("has_existing") == "Yes" and pending_amount > 0:
        months = max(1, int(session.get("pending_years", 1)) * 12)
        principal_base = float(pending_amount)
    else:
        months = loan_years * 12
        principal_base = float(user_profile.get("loan_amount", 0))

    new_interest_series = []
    if months > 0 and principal_base > 0:
        assumed_annual_rate = chosen_new_rate
        risk_penalty = 0.0
        if risk == "Medium":
            risk_penalty = 1.5
        elif risk == "High":
            risk_penalty = 3.5

        adjusted_rate = assumed_annual_rate + risk_penalty
        monthly_rate = adjusted_rate / 12 / 100

        balance = principal_base
        principal_payment = balance / months
        cumulative = 0.0
        for m in range(1, months + 1):
            interest_m = balance * monthly_rate
            cumulative += interest_m
            balance -= principal_payment

            if m % 12 == 0:
                new_interest_series.append(round(cumulative, 2))

        while len(new_interest_series) < len(interest_years):
            new_interest_series.append(
                new_interest_series[-1] if new_interest_series else 0.0)
    else:
        new_interest_series = [0 for _ in interest_years]

    # cumulative existing interest projected over pending_years (if present)
    if pending_years > 0 and existing_interest > 0:
        existing_interest_series = [
            round(existing_interest * min(1.0, yr / pending_years), 2)
            for yr in interest_years
        ]
    else:
        existing_interest_series = [0 for _ in interest_years]

    # ---------------- RENDER ----------------
    return render_template(
        "result.html",
        risk=risk,
        risk_score=risk_score,
        advisory=advisory,
        rule_reasons=rule_reasons,
        loans=loans,
        best_loan=best_loan,
        top_loans=top_loans,
        pending_amount=pending_amount,
        existing_interest=existing_interest,
        new_interest=new_interest,
        refinance_interest=refinance_interest,
        using_refinance=(session.get("has_existing") ==
                         "Yes" and pending_amount > 0),
        savings_percent=savings_percent,
        interest_years=interest_years,
        new_interest_series=new_interest_series,
        existing_interest_series=existing_interest_series
    )


# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
