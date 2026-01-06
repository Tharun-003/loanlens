import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from trainer_utils import clean_and_save_encoders, evaluate_and_train, print_detailed_eval

# 1. Load Data
df = pd.read_csv('../data/raw/final_education_loans.csv')

# 2. Clean and Encode
processed_df = clean_and_save_encoders(df, 'education')

# 3. Features & Target
X = processed_df.drop('approval_status', axis=1)
y = processed_df['approval_status']

# 4. Stratified Split (VERY IMPORTANT)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. High-Accuracy Model (Industry Standard)
model = RandomForestClassifier(
    n_estimators=200,        # Strong ensemble
    max_depth=8,             # Prevents overfitting
    min_samples_leaf=5,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)

# 6. Cross-Validated Training
model = evaluate_and_train(model, X_train, y_train, nfolds=5)

# 7. Evaluation
print_detailed_eval(model, X_test, y_test)

# 8. Save Model
with open('../models/education_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"\n✅ FINAL ACCURACY: {model.score(X_test, y_test):.2%}")
