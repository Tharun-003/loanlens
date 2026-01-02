import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Path to your dataset
# If the file is inside your 'data' folder, use 'data/filename.csv'
filename = 'education_loans.xlsx - Sheet1.csv' 

if not os.path.exists(filename):
    print(f"Error: Could not find {filename}")
    print("If it is inside the 'data' folder, change the filename in the code to 'data/filename.csv'")
else:
    df = pd.read_csv(filename)

    # 2. Preprocessing
    df_clean = df.drop(['loan_type', 'moratorium_applicable'], axis=1)
    df_processed = pd.get_dummies(df_clean, columns=[
        'bank_name', 'course_level', 'course_type', 
        'study_country', 'college_tier'
    ], drop_first=True)

    # 3. Features and Target
    X = df_processed.drop('approval_status', axis=1)
    y = df_processed['approval_status']

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Train
    print("Training the Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # 6. Test/Evaluate
    y_pred = rf_model.predict(X_test)
    print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 7. Save to your 'model' folder (which I see in your directory list)
    model_path = 'model/loan_rf_model.pkl'
    feature_path = 'model/model_features.pkl'
    
    joblib.dump(rf_model, model_path)
    joblib.dump(X.columns.tolist(), feature_path)
    
    print(f"\nSuccess! Model saved in {model_path}")