from flask import Flask, render_template, request, redirect, session
import pickle
import numpy as np

# Corrected imports (Ensures no typos in logic folder)
from logic.risk_analaysis import calculate_risk
from logic.loan_recommender import recommend_loans
from logic.interest_calculator import calculate_pending_interest
from logic.rule_eligibility import rule_based_eligibility

app = Flask(__name__)
app.secret_key = "finsense_secret_key"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/loan-purpose")
    return render_template("login.html")

@app.route("/loan-purpose", methods=["GET", "POST"])
def loan_purpose():
    if request.method == "POST":
        session["loan_type"] = request.form["loan_type"]
        return redirect("/personal-details")
    return render_template("loan_purpose.html")

@app.route("/personal-details", methods=["GET", "POST"])
def personal_details():
    if request.method == "POST":
        session["age"] = int(request.form["age"])
        session["income_annum"] = int(request.form["monthly_income"]) * 12
        session["cibil_score"] = int(request.form["credit_score"])
        session["loan_amount"] = int(request.form["loan_amount"])
        session["loan_term"] = int(request.form["loan_tenure"])
        session["res_assets"] = int(request.form.get("res_assets", 0))
        session["comm_assets"] = int(request.form.get("comm_assets", 0))
        return redirect("/existing-loan")
    return render_template("personal_details.html")

@app.route("/existing-loan", methods=["GET", "POST"])
def existing_loan():
    if request.method == "POST":
        has_loan = request.form["has_existing_loan"]
        session["has_existing_loan"] = True if has_loan == "yes" else False
        if session["has_existing_loan"]:
            session["interest_rate"] = float(request.form["interest_rate"])
            session["pending_amount"] = int(request.form["pending_amount"])
            session["remaining_months"] = int(request.form["remaining_years"]) * 12
        return redirect("/result")
    return render_template("existing_loan.html")

@app.route("/result")
def result():
    user_profile = {
        "loan_type": session.get("loan_type"),
        "income_annum": session.get("income_annum", 0),
        "loan_amount": session.get("loan_amount", 0),
        "cibil_score": session.get("cibil_score", 0),
        "loan_term": session.get("loan_term", 0),
        "residential_assets_value": session.get("res_assets", 0),
        "commercial_assets_value": session.get("comm_assets", 0)
    }

    # 1. AI Analysis & Advisory
    risk_level, risk_explanation = calculate_risk(user_profile)
    advisory, rule_reasons = rule_based_eligibility(user_profile, risk_level)
    
    # 2. Bank Suggestions (Filtered from Dataset)
    recommendations = recommend_loans(user_profile, risk_level)

    # 3. Interest Calculation (Risk-Adjusted)
    pending_interest_data = None
    if session.get("has_existing_loan"):
        pending_interest_data = calculate_pending_interest(
            session["pending_amount"],
            session["interest_rate"],
            session["remaining_months"],
            risk_level
        )

    return render_template(
        "result.html",
        risk_level=risk_level,
        risk_explanation=risk_explanation,
        advisory=advisory,
        rule_reasons=rule_reasons,
        loans=recommendations,
        pending_interest=pending_interest_data
    )

if __name__ == "__main__":
    app.run(debug=True)