import os
import pickle
import pandas as pd
import sys

# Add project root to path
sys.path.append(os.getcwd())

from logic.ml_mangement import load_model

def inspect_models():
    loan_types = ["Education Loan", "Home Loan", "Personal Loan"]
    
    for loan_type in loan_types:
        print(f"\n--- Inspecting {loan_type} Model ---")
        try:
            model = load_model(loan_type)
            if hasattr(model, "feature_names_in_"):
                print("Feature Names:", list(model.feature_names_in_))
            else:
                print("Model does not have feature_names_in_ attribute.")
                
            # Check for scaler/encoders if possible?
            # actually just knowing the feature names is enough to compare with app.py input
            
        except Exception as e:
            print(f"Error loading {loan_type}: {e}")

if __name__ == "__main__":
    inspect_models()
