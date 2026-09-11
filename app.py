from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

COMMON = {
    "password", "password123", "123456", "12345678", "123456789",
    "qwerty", "qwerty123", "admin", "admin123", "welcome", "letmein",
    "abc123", "iloveyou", "monkey", "football"
}

def analyze_password(password):
    score = 0
    weaknesses = []
    recommendations = []

    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    if length >= 16:
        score += 35
    elif length >= 12:
        score += 28
    elif length >= 8:
        score += 18
    elif length > 0:
        score += 8

    if has_upper: score += 12
    if has_lower: score += 12
    if has_digit: score += 12
    if has_special: score += 15

    lower = password.lower()

    if lower in COMMON:
        score = min(score, 25)
        weaknesses.append("This password matches a commonly used password.")
        recommendations.append("Choose a unique password that is not commonly used.")

    if re.search(r"(123|234|345|456|567|678|789|abc|qwerty)", lower):
        score = max(0, score - 15)
        weaknesses.append("A predictable sequence or keyboard pattern was detected.")
        recommendations.append("Avoid predictable sequences such as 123 or abc.")

    if re.search(r"(.)\1\1", password):
        score = max(0, score - 8)
        weaknesses.append("Repeated characters reduce unpredictability.")
        recommendations.append("Avoid repeating the same character several times.")

    if length < 12:
        weaknesses.append("Password length is below the recommended 12+ characters.")
        recommendations.append("Use a longer password or passphrase.")

    if not has_upper:
        weaknesses.append("No uppercase letter detected.")
        recommendations.append("Add uppercase letters where appropriate.")

    if not has_lower:
        weaknesses.append("No lowercase letter detected.")
        recommendations.append("Include lowercase letters.")

    if not has_digit:
        weaknesses.append("No number detected.")
        recommendations.append("Include numbers.")

    if not has_special:
        weaknesses.append("No special character detected.")
        recommendations.append("Include a special character such as !, @, or #.")

    score = min(100, max(0, score))

    if score >= 75:
        level = "Strong"
        label = "LOW RISK"
        color = "green"
    elif score >= 45:
        level = "Medium"
        label = "MODERATE RISK"
        color = "orange"
    else:
        level = "Weak"
        label = "HIGH RISK"
        color = "red"

    # Demonstration confidence value based on how many security signals are present.
    signals = sum([has_upper, has_lower, has_digit, has_special, length >= 12])
    confidence = min(99, 70 + signals * 5)

    checks = {
        "Good length": length >= 12,
        "Uppercase": has_upper,
        "Lowercase": has_lower,
        "Numbers": has_digit,
        "Special characters": has_special,
    }

    return {
        "score": score,
        "level": level,
        "label": label,
        "color": color,
        "confidence": confidence,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "checks": checks
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not password:
        return jsonify({"error": "Please enter a password."}), 400
    return jsonify(analyze_password(password))

if __name__ == "__main__":
    app.run(debug=True)
