from flask import Flask, render_template, request, jsonify
from datetime import datetime
from utils.db import users_collection, predictions_collection
from utils.auth import register_user, login_user
from utils.analytics import get_admin_analytics

app = Flask(__name__)


# -------------------------
# SIMULATED ML MODEL
# -------------------------

def calculate_churn_probability(
    tenure,
    watch_hours,
    days_since_login,
    subscription_type,
    tickets_raised,
    profiles_used
):

    tenure_norm = min(tenure / 36.0, 1.0)
    watch_norm = min(watch_hours / 40.0, 1.0)
    days_norm = min(days_since_login / 30.0, 1.0)
    tickets_norm = min(tickets_raised / 5.0, 1.0)
    profiles_norm = min(profiles_used / 5.0, 1.0)

    sub_bonus = {
        "basic": 0.0,
        "standard": 0.05,
        "premium": 0.10
    }

    loyalty_bonus = sub_bonus.get(subscription_type.lower(), 0.05)

    churn_score = (
        0.30 * (1 - tenure_norm) +
        0.35 * (1 - watch_norm) +
        0.20 * days_norm +
        0.10 * tickets_norm -
        0.15 * profiles_norm -
        loyalty_bonus
    )

    probability = max(0.03, min(0.95, churn_score))
    return round(probability, 3)


# -------------------------
# PAGE ROUTES
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


# -------------------------
# AUTH
# -------------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    result = register_user(data)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = login_user(data)

    if not result["success"]:
        return jsonify(result), 401

    return jsonify(result)


# -------------------------
# PREDICT
# -------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    inputs = data.get("inputs", {})

    probability = calculate_churn_probability(
        float(inputs.get("tenure", 12)),
        float(inputs.get("watch_hours", 10)),
        float(inputs.get("days_since_login", 5)),
        inputs.get("subscription_type", "standard"),
        float(inputs.get("tickets_raised", 1)),
        float(inputs.get("profiles_used", 2))
    )

    risk = "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"

    suggestion = (
        "Offer Premium trial" if risk == "High"
        else "Send recommendation" if risk == "Medium"
        else "No action required"
    )

    record = {
        "user": email,
        "probability": probability,
        "risk": risk,
        "suggestion": suggestion,
        "inputs": inputs,
        "created_at": datetime.utcnow()
    }

    predictions_collection.insert_one(record)

    return jsonify({
        "probability": probability,
        "risk": risk,
        "suggestion": suggestion
    })


# -------------------------
# USER HISTORY
# -------------------------

@app.route("/user-data/<email>")
def user_data(email):

    records = list(
        predictions_collection
        .find({"user": email})
        .sort("created_at", -1)
    )

    formatted = []
    for r in records:
        formatted.append({
            "_id": str(r["_id"]),
            "probability": r["probability"],
            "risk": r["risk"],
            "suggestion": r["suggestion"],
            "created_at": r["created_at"].isoformat()
        })

    return jsonify(formatted)


# -------------------------
# ADMIN ANALYTICS
# -------------------------

@app.route("/admin-data")
def admin_data():
    return jsonify(get_admin_analytics())


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
