import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import classification_report, confusion_matrix

def clean_and_save_encoders(df, prefix):
    """
    Cleans data and encodes categorical variables. 
    Saves encoders to prevent data leakage and handle new data.
    """
    df = df.copy()
    # Fill missing values to stabilize the model
    df = df.ffill().bfill()
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        # Save encoder for future use in the web app
        with open(f'../models/{prefix}_{col}_encoder.pkl', 'wb') as f:
            pickle.dump(le, f)
            
    return df

def evaluate_and_train(model, X, y, nfolds=5):
    """
    Uses K-Fold Cross-Validation to ensure the model generalizes well.
    """
    kf = KFold(n_splits=nfolds, shuffle=True, random_state=42)
    # Using cross_val_score to get a realistic accuracy estimate
    cv_scores = cross_val_score(model, X, y, cv=kf)
    
    print(f"\n--- Cross-Validation Report ({nfolds} Folds) ---")
    print(f"Average Accuracy: {np.mean(cv_scores):.2%}")
    print(f"Score Variance: {np.std(cv_scores):.4f}")
    
    # Train the final version of the model on all provided data
    model.fit(X, y)
    return model

def print_detailed_eval(model, X_test, y_test):
    """
    Prints precision and recall to identify if the model is biased.
    """
    y_pred = model.predict(X_test)
    print("\n--- Detailed Classification Report ---")
    print(classification_report(y_test, y_pred))