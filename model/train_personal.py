import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from trainer_utils import clean_and_save_encoders

# 1. Load Data
df = pd.read_csv('../data/raw/final_personal_loan.csv')

# 2. Clean
processed_df = clean_and_save_encoders(df, 'personal')

# 3. Define Features (X) and Target (y)
X = processed_df.drop('approval_status', axis=1)
y = processed_df['approval_status']

# 4. Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train Decision Tree
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 6. Save Model
with open('../models/personal_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Personal Model Trained. Test Accuracy: {model.score(X_test, y_test):.2%}")