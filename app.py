from flask import Flask, render_template, request, redirect, url_for, session

# ✅ IMPORT LOGIC
from logic.loan_recommender import recommend_loans
from logic.risk_analaysis import calculate_risk
from logic.interest_calculator import calculate_pending_interest
from logic.rule_eligibility import rule_based_eligibility


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "loanlens_secret_key"


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
        "loan_tenure": session.get("loan_tenure", 1),
        "property_value": session.get("property_value", 0),
        "down_payment": session.get("down_payment", 0),
        "study_country": session.get("study_country", ""),
        "employment_type": session.get("employment_type", ""),
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

    # ---------------- INTEREST CALCULATIONS ----------------
    pending_amount = session.get("pending_amount", 0)

    # New loan interest (simple & realistic)
    new_interest = user_profile["loan_amount"] * \
        0.08 * user_profile["loan_tenure"]

    existing_interest = 0
    savings_percent = 0

    if session.get("has_existing") == "Yes" and pending_amount > 0:
        interest_data = calculate_pending_interest(
            principal=pending_amount,
            annual_rate=session.get("old_interest", 0),
            total_months=session.get("pending_years", 1) * 12,
            risk_level=risk
        )

        # Handle dict OR number safely
        existing_interest = (
            interest_data.get("pending_interest", 0)
            if isinstance(interest_data, dict)
            else float(interest_data)
        )

        if existing_interest > 0:
            savings_percent = round(
                ((existing_interest - new_interest) / existing_interest) * 100, 2
            )

    # ---------------- RENDER ----------------
    return render_template(
        "result.html",
        risk=risk,
        risk_score=risk_score,
        advisory=advisory,
        rule_reasons=rule_reasons,
        loans=loans,
        best_loan=best_loan,
        pending_amount=pending_amount,
        existing_interest=existing_interest,
        new_interest=new_interest,
        savings_percent=savings_percent
    )


# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
