import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# -----------------------------------
# 1️⃣ LOAD TRAINING DATA
# -----------------------------------
# Make sure this file exists in data/
df = pd.read_csv("data/user_training_data.csv")

# -----------------------------------
# 2️⃣ FEATURE / TARGET SPLIT
# -----------------------------------
X = df.drop("eligibility", axis=1)
y = df["eligibility"]

# -----------------------------------
# 3️⃣ TRAIN-TEST SPLIT
# -----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------------
# 4️⃣ MODEL INITIALISATION
# -----------------------------------
model = LogisticRegression(
    max_iter=1000,
    solver="liblinear"
)

# -----------------------------------
# 5️⃣ TRAIN MODEL
# -----------------------------------
model.fit(X_train, y_train)

# -----------------------------------
# 6️⃣ EVALUATE MODEL
# -----------------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------------
# 7️⃣ SAVE TRAINED MODEL
# -----------------------------------
joblib.dump(model, "model/eligibility_model.pkl")

print("\n✅ Model trained and saved as model/eligibility_model.pkl")
