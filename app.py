from flask import Flask, render_template, request, redirect, session

from logic.risk_analaysis import calculate_risk
from logic.loan_recommender import recommend_loans
from logic.interest_calculator import calculate_pending_interest
from logic.rule_eligibility import rule_based_eligibility

app = Flask(__name__)
app.secret_key = "loanlens_secret"


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/select-loan")
    return render_template("login.html")


# ---------------- SELECT LOAN ----------------
@app.route("/select-loan", methods=["GET", "POST"])
def select_loan():
    if request.method == "POST":
        session["loan_type"] = request.form.get("loan_type")
        return redirect("/loan-purpose")
    return render_template("select_loan.html")


# ---------------- LOAN PURPOSE ----------------
@app.route("/loan-purpose", methods=["GET", "POST"])
def loan_purpose():
    if request.method == "POST":
        session["loan_type"] = request.form.get("loan_type")
        return redirect("/personal-details")
    return render_template("loan_purpose.html")


# ---------------- PERSONAL DETAILS ----------------
@app.route("/personal-details", methods=["GET", "POST"])
def personal_details():
    if request.method == "POST":
        session["income"] = int(request.form.get("income", 0))
        session["credit_score"] = int(request.form.get("credit_score", 0))

        # New loan details (FOR AWARENESS)
        session["new_loan_amount"] = int(request.form.get("new_loan_amount", 0))
        session["new_loan_tenure"] = int(request.form.get("new_loan_tenure", 0))

        return redirect("/existing-loan")

    return render_template("personal_details.html")


# ---------------- EXISTING LOAN ----------------
@app.route("/existing-loan", methods=["GET", "POST"])
def existing_loan():
    if request.method == "POST":
        has_existing = (request.form.get("has_existing") or "").strip()
        session["has_existing"] = has_existing

        if has_existing == "Yes":
            session["pending_amount"] = int(
                request.form.get("pending_amount") or 0
            )

            session["existing_interest_rate"] = float(
                request.form.get("existing_interest_rate") or 0
            )

            session["remaining_months"] = int(
                request.form.get("remaining_tenure") or 0
            ) * 12
        else:
            session["pending_amount"] = 0
            session["existing_interest_rate"] = 0.0
            session["remaining_months"] = 0

        return redirect("/recommendation")

    return render_template("existing_loan.html")


# ---------------- RECOMMENDATION (LOADING) ----------------
@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    # -------- USER PROFILE (MODEL INPUT) --------
    user_profile = {
        "income": session.get("income", 0),
        "credit_score": session.get("credit_score", 0),
        "loan_type": session.get("loan_type") or "Unknown",
        "new_loan_amount": session.get("new_loan_amount", 0),
        "new_loan_tenure": session.get("new_loan_tenure", 0),
    }

    # -------- RISK ANALYSIS --------
    risk, risk_score = calculate_risk(user_profile)

    # -------- RULE-BASED ELIGIBILITY --------
    advisory, rule_reasons = rule_based_eligibility(user_profile, risk)

    # -------- LOAN RECOMMENDATION MODEL --------
    loans = recommend_loans(user_profile, risk)

    # -------- EXISTING LOAN INTEREST MODEL --------
    pending_interest = None
    if session.get("has_existing") == "Yes":
        pending_interest = calculate_pending_interest(
            principal=session.get("pending_amount", 0),
            annual_rate=session.get("existing_interest_rate", 0),
            total_months=session.get("remaining_months", 0),
            risk_level=risk
        )

    return render_template(
        "result.html",
        risk=risk,
        risk_score=risk_score,
        income=user_profile["income"],
        credit_score=user_profile["credit_score"],
        advisory=advisory,
        rule_reasons=rule_reasons,
        loans=loans,
        pending_interest=pending_interest
    )


if __name__ == "__main__":
    app.run(debug=True)
