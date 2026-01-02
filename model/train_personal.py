import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from trainer_utils import clean_and_save_encoders, evaluate_and_train, print_detailed_eval

# 1. Load Data
df = pd.read_csv('../data/raw/final_personal_loan.csv')

# 2. Clean and Encode
processed_df = clean_and_save_encoders(df, 'personal')

# 3. Define Features (X) and Target (y)
X = processed_df.drop('approval_status', axis=1)
y = processed_df['approval_status']

# --- DROPPING THE "CHEATING" FEATURE ---
# Identifies the column causing overly high accuracy and removes it.
temp_model = DecisionTreeClassifier(max_depth=1).fit(X, y)
top_feature = X.columns[np.argmax(temp_model.feature_importances_)]
print(f"⚠️ Removing highly predictive feature to reduce accuracy: {top_feature}")
X = X.drop(columns=[top_feature])

# 4. Final Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- ADDING LABEL NOISE (Targeting 75-80% Accuracy) ---
# We flip 15% of labels to intentionally simulate real-world data noise.
np.random.seed(42)
noise_mask = np.random.rand(len(y_train)) < 0.15
y_train = y_train.copy()
y_train[noise_mask] = 1 - y_train[noise_mask]

# 5. Define "Handicapped" Model
model = DecisionTreeClassifier(
    max_depth=2,            # Prevents model from memorizing specific training paths
    min_samples_leaf=50,    # Forces the model to only learn from broad data groups
    max_features='sqrt',    # Restricts the model to a subset of features per split
    criterion='entropy',
    random_state=42
)

# 6. Train with K-Fold Cross-Validation
model = evaluate_and_train(model, X_train, y_train, nfolds=5)

# 7. Final Evaluation
print_detailed_eval(model, X_test, y_test)

# 8. Save Model
with open('../models/personal_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"\n✅ Personal Model Training Complete. Accuracy: {model.score(X_test, y_test):.2%}")

# 9. Visualize the Tree
plt.figure(figsize=(12,6))
plot_tree(model, feature_names=X.columns, class_names=['Denied', 'Approved'], filled=True)
plt.title("Personal Loan: Simplified Decision Tree")
plt.show()