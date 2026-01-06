import os
import pickle
import pandas as pd

# ---------------- PROJECT ROOT ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- MODELS ----------------
MODELS = {
    "Education Loan": ("education_model.pkl", "education"),
    "Home Loan": ("home_model.pkl", "home"),
    "Personal Loan": ("personal_model.pkl", "personal"),
}

# ---------------- LOAD MODEL ----------------
def load_model(loan_name):
    model_file, _ = MODELS[loan_name]
    path = os.path.join(BASE_DIR, "models", model_file)
    with open(path, "rb") as f:
        return pickle.load(f)

# ---------------- LOAD ENCODER ----------------
def load_encoder(prefix, col):
    path = os.path.join(BASE_DIR, "models", f"{prefix}_{col}_encoder.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

# ---------------- PREPROCESS USER DATA ----------------
def preprocess_user_data(user_profile, loan_name):
    """
    Builds ML-ready input strictly aligned with the trained dataset.
    Handles unseen categorical values safely.
    """

    model_file, prefix = MODELS[loan_name]
    model = load_model(loan_name)

    row = {}

    for col in model.feature_names_in_:
        encoder = load_encoder(prefix, col)

        if col in user_profile:
            value = user_profile[col]

            if encoder:
                value = str(value)
                if value not in encoder.classes_:
                    value = encoder.classes_[0]  # fallback to known class
                row[col] = encoder.transform([value])[0]
            else:
                row[col] = value
        else:
            # Safe default
            if encoder:
                row[col] = encoder.transform([encoder.classes_[0]])[0]
            else:
                row[col] = 0

    return pd.DataFrame([row], columns=model.feature_names_in_)
