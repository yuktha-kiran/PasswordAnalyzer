from flask import Flask, render_template, request, jsonify
import joblib

from feature_extractor import extract_features, FEATURE_NAMES

app = Flask(__name__)

# Load trained ML model
MODEL_PATH = "model/password_model.pkl"

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
feature_names = model_data["features"]


COMMON_PASSWORDS = {
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
    "test123",
}


def analyze_password(password):

    # Extract features
    features = extract_features(password)
    feature_values = dict(zip(FEATURE_NAMES, features))

    # Arrange features exactly as the model expects
    model_input = [
        feature_values[name]
        for name in feature_names
    ]

    # ML prediction
    prediction = model.predict([model_input])[0]

    # ML confidence
    probabilities = model.predict_proba([model_input])[0]
    classes = model.classes_

    probability_map = dict(zip(classes, probabilities))
    confidence = probability_map.get(prediction, 0) * 100

    # --------------------------------------------------
    # Security checks
    # --------------------------------------------------

    checks = {
        "Minimum Length": len(password) >= 8,
        "Uppercase Letter": feature_values["has_uppercase"],
        "Lowercase Letter": feature_values["has_lowercase"],
        "Number": feature_values["has_digit"],
        "Special Character": feature_values["has_special"],
        "No Common Password": not feature_values["is_common_password"],
        "No Predictable Sequence": not feature_values["has_sequence"],
        "No Excessive Repetition": not feature_values["has_repeated_characters"],
    }

    # --------------------------------------------------
    # Calculate a user-friendly security score
    # --------------------------------------------------

    score = 0

    # Length
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 18
    elif len(password) >= 6:
        score += 10

    # Character diversity
    if feature_values["has_uppercase"]:
        score += 12

    if feature_values["has_lowercase"]:
        score += 12

    if feature_values["has_digit"]:
        score += 12

    if feature_values["has_special"]:
        score += 15

    # Uniqueness
    if feature_values["unique_characters"] >= 8:
        score += 12

    # Security penalties
    if feature_values["is_common_password"]:
        score -= 30

    if feature_values["has_sequence"]:
        score -= 10

    if feature_values["has_repeated_characters"]:
        score -= 5

    score = max(0, min(100, score))

    # --------------------------------------------------
    # Weaknesses and recommendations
    # --------------------------------------------------

    weaknesses = []
    recommendations = []

    if len(password) < 8:
        weaknesses.append("Password is shorter than 8 characters.")
        recommendations.append("Use at least 12 characters.")

    elif len(password) < 12:
        weaknesses.append("Password length could be improved.")
        recommendations.append("Consider using 12 or more characters.")

    if not feature_values["has_uppercase"]:
        weaknesses.append("No uppercase letters detected.")
        recommendations.append("Add uppercase letters.")

    if not feature_values["has_lowercase"]:
        weaknesses.append("No lowercase letters detected.")
        recommendations.append("Add lowercase letters.")

    if not feature_values["has_digit"]:
        weaknesses.append("No numbers detected.")
        recommendations.append("Add numbers.")

    if not feature_values["has_special"]:
        weaknesses.append("No special characters detected.")
        recommendations.append(
            "Add symbols such as !, @, #, or $."
        )

    if feature_values["is_common_password"]:
        weaknesses.append(
            "Password matches a commonly used password."
        )
        recommendations.append(
            "Avoid common passwords and predictable patterns."
        )

    if feature_values["has_sequence"]:
        weaknesses.append(
            "Sequential or predictable character patterns detected."
        )
        recommendations.append(
            "Avoid patterns such as 123, abc, qwerty, or similar sequences."
        )

    if feature_values["has_repeated_characters"]:
        weaknesses.append(
            "Repeated characters detected."
        )
        recommendations.append(
            "Avoid excessive repetition of the same character."
        )

    if not weaknesses:
        recommendations.append(
            "Use a unique password and avoid reusing it across accounts."
        )

    # --------------------------------------------------
    # Risk level
    # --------------------------------------------------

    if prediction == "Strong":
        risk = "Low Risk"
        risk_class = "low"

    elif prediction == "Medium":
        risk = "Moderate Risk"
        risk_class = "medium"

    else:
        risk = "High Risk"
        risk_class = "high"

    return {
        "score": score,
        "level": prediction,
        "risk": risk,
        "risk_class": risk_class,
        "confidence": round(confidence, 2),
        "checks": checks,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "features": feature_values,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "password" not in data:
        return jsonify({
            "error": "Password field is required."
        }), 400

    password = data["password"]

    if not isinstance(password, str):
        return jsonify({
            "error": "Password must be text."
        }), 400

    if not password:
        return jsonify({
            "error": "Please enter a password."
        }), 400

    try:
        result = analyze_password(password)
        return jsonify(result)

    except Exception as e:
        print("Analysis error:", e)

        return jsonify({
            "error": "Unable to analyze the password."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)