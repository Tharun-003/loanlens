from flask import Flask, render_template, request, redirect, session

from logic.risk_analaysis import calculate_risk
from logic.loan_recommender import recommend_loans
from logic.interest_calculator import calculate_pending_interest

app = Flask(__name__)
app.secret_key = "finsense_secret_key"

# -----------------------------------
# 1️⃣ LOGIN PAGE
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/loan-purpose")
    return render_template("login.html")


# -----------------------------------
# 2️⃣ LOAN PURPOSE PAGE
# -----------------------------------
@app.route("/loan-purpose", methods=["GET", "POST"])
def loan_purpose():
    if request.method == "POST":
        session["loan_type"] = request.form["loan_type"]
        return redirect("/personal-details")
    return render_template("loan_purpose.html")


# -----------------------------------
# 3️⃣ PERSONAL & FINANCIAL DETAILS
# -----------------------------------
@app.route("/personal-details", methods=["GET", "POST"])
def personal_details():
    if request.method == "POST":
        session["age"] = int(request.form["age"])
        session["monthly_income"] = int(request.form["monthly_income"])
        session["monthly_expenses"] = int(request.form["monthly_expenses"])
        session["credit_score"] = int(request.form["credit_score"])
        session["loan_amount"] = int(request.form["loan_amount"])
        session["loan_tenure"] = int(request.form["loan_tenure"])

        return redirect("/existing-loan")

    return render_template("personal_details.html")


# -----------------------------------
# 4️⃣ EXISTING LOAN DETAILS
# -----------------------------------
@app.route("/existing-loan", methods=["GET", "POST"])
def existing_loan():
    if request.method == "POST":
        has_loan = request.form["has_existing_loan"]
        session["has_existing_loan"] = True if has_loan == "yes" else False

        if session["has_existing_loan"]:
            session["existing_loan_type"] = request.form["existing_loan_type"]
            session["original_amount"] = int(request.form["original_amount"])
            session["interest_rate"] = float(request.form["interest_rate"])
            session["pending_amount"] = int(request.form["pending_amount"])
            session["remaining_years"] = int(request.form["remaining_years"])

        return redirect("/result")

    return render_template("existing_loan.html")


# -----------------------------------
# 5️⃣ RESULT PAGE (FINAL OUTPUT)
# -----------------------------------
@app.route("/result")
def result():

    user_data = {
        "loan_type": session["loan_type"],
        "age": session["age"],
        "monthly_income": session["monthly_income"],
        "monthly_expenses": session["monthly_expenses"],
        "credit_score": session["credit_score"],
        "loan_amount": session["loan_amount"],
        "loan_tenure": session["loan_tenure"],
        "has_existing_loan": session["has_existing_loan"]
    }

    # --- Risk Analysis ---
    risk_level, risk_reasons = calculate_risk(user_data)

    # --- Loan Recommendations (DATASET ONLY) ---
    recommended_loans = recommend_loans(
        loan_type=user_data["loan_type"],
        credit_score=user_data["credit_score"],
        monthly_income=user_data["monthly_income"],
        loan_tenure=user_data["loan_tenure"],
        risk_level=risk_level,
        has_existing_loan=user_data["has_existing_loan"]
    )

    # --- Pending Interest Awareness ---
    pending_interest = None
    if session["has_existing_loan"]:
        pending_interest = calculate_pending_interest(
            session["pending_amount"],
            session["interest_rate"],
            session["remaining_years"]
        )

    # --- Advisory Message ---
    if risk_level == "Low Risk":
        advisory = "Recommended"
    elif risk_level == "Medium Risk":
        advisory = "Proceed with caution"
    else:
        advisory = "Not advisable currently"

    return render_template(
        "result.html",
        user=user_data,
        risk_level=risk_level,
        risk_reasons=risk_reasons,
        advisory=advisory,
        loans=recommended_loans,
        pending_interest=pending_interest,
        session=session
    )


# -----------------------------------
# RUN APP
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
