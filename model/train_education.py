import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
# This line will now work correctly
from trainer_utils import clean_and_save_encoders, evaluate_and_train, print_detailed_eval

# 1. Load Data
df = pd.read_csv('../data/raw/final_education_loans.csv')

# 2. Clean and Encode
processed_df = clean_and_save_encoders(df, 'education')

# 3. Split Data
X = processed_df.drop('approval_status', axis=1)
y = processed_df['approval_status']

# Split into Training and a final "Holdout" set for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Define Model with Pruning (to reduce overfitting)
# We limit max_depth and set min_samples_leaf to simplify the model
model = DecisionTreeClassifier(
    max_depth=2,            # Only allow 2 "questions" total. This will drop accuracy significantly.
    min_samples_leaf=50,    # Requires a huge group (50+) to agree before making a rule.
    max_features='sqrt',    # Only look at a random few features at each split.
    random_state=42
)

# 5. Train with K-Fold Cross-Validation
model = evaluate_and_train(model, X_train, y_train, nfolds=5)

# 6. Final Evaluation on unseen data
print_detailed_eval(model, X_test, y_test)

# 7. Save Model
with open('../models/education_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"\n✅ Training Complete. Final Holdout Accuracy: {model.score(X_test, y_test):.2%}")
plt.figure(figsize=(20,10))
plot_tree(model, feature_names=X.columns, class_names=['Denied', 'Approved'], filled=True)
plt.show()
