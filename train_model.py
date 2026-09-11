import os
import random
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from feature_extractor import extract_features, FEATURE_NAMES


# ---------------------------------------------------------
# 1. Generate a labeled educational password dataset
# ---------------------------------------------------------

random.seed(42)

weak_passwords = [
    "123456",
    "12345678",
    "password",
    "password123",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "letmein",
    "abc123",
    "hello123",
    "football",
    "monkey",
    "iloveyou",
    "111111",
    "123123",
    "000000",
    "pass123",
    "test123"
]

medium_passwords = [
    "Hello123",
    "Welcome12",
    "Student2026",
    "Python1234",
    "Network2026",
    "College@123",
    "Security123",
    "Project2026",
    "Computer@12",
    "Science2026",
    "Password@12",
    "Karnataka123",
    "Cyber1234",
    "Flask@123",
    "Learning2026",
    "Student@2026",
    "Secure123!",
    "MyProject12",
    "Cloud@2026",
    "Coding123!"
]

strong_passwords = [
    "Moon!River#84Cloud",
    "Blue$Forest27!Stone",
    "Quantum#Lake91@Pine",
    "Silver!Tiger84$Cloud",
    "River@Stone#72Moon",
    "Cedar!Ocean49#Light",
    "Falcon$River82!Star",
    "Cloud#Garden64@Stone",
    "Maple!Thunder38$Sky",
    "Crystal@Forest71#Wave",
    "Sunset#Mountain93!Leaf",
    "Winter$Ocean58@Flame",
    "Golden!River26#Cloud",
    "Aurora@Stone83$Forest",
    "Thunder#Garden47!Moon",
    "Velvet$Ocean62@Star",
    "Forest!Crystal39#Lake",
    "Planet@River75$Cloud",
    "Shadow#Mountain48!Tree",
    "Comet!Garden86@Stone"
]


passwords = (
    [(p, "Weak") for p in weak_passwords]
    + [(p, "Medium") for p in medium_passwords]
    + [(p, "Strong") for p in strong_passwords]
)


# ---------------------------------------------------------
# 2. Convert passwords into ML features
# ---------------------------------------------------------

rows = []

for password, label in passwords:
    features = extract_features(password)

    row = dict(zip(FEATURE_NAMES, features))
    row["password"] = password
    row["label"] = label

    rows.append(row)


df = pd.DataFrame(rows)

# Save the dataset
os.makedirs("data", exist_ok=True)

dataset_path = "data/password_dataset.csv"
df.to_csv(dataset_path, index=False)

print(f"\nDataset saved to: {dataset_path}")
print(f"Total samples: {len(df)}")
print("\nClass distribution:")
print(df["label"].value_counts())


# ---------------------------------------------------------
# 3. Prepare data for Machine Learning
# ---------------------------------------------------------

X = df[FEATURE_NAMES]
y = df["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# 4. Train Random Forest classifier
# ---------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ---------------------------------------------------------
# 5. Evaluate the model
# ---------------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 50)
print("MODEL EVALUATION")
print("=" * 50)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))


# ---------------------------------------------------------
# 6. Display feature importance
# ---------------------------------------------------------

importance = pd.DataFrame({
    "Feature": FEATURE_NAMES,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nFeature Importance:")
print(importance.to_string(index=False))


# ---------------------------------------------------------
# 7. Save the trained model
# ---------------------------------------------------------

os.makedirs("model", exist_ok=True)

model_path = "model/password_model.pkl"

joblib.dump(
    {
        "model": model,
        "features": FEATURE_NAMES
    },
    model_path
)

print("\n" + "=" * 50)
print(f"Trained model saved to: {model_path}")
print("=" * 50)