from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
from utils.db import users_collection, predictions_collection
from utils.auth import register_user, login_user
from utils.analytics import get_admin_analytics
import csv
import os
import pandas as pd

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
# SINGLE PREDICT (STORES IN DB)
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
            "probability": r.get("probability", 0),
            "risk": r.get("risk", "Unknown"),
            "suggestion": r.get("suggestion", "N/A"),
            "created_at": r["created_at"].isoformat()
            if r.get("created_at") else ""
        })

    return jsonify(formatted)


# -------------------------
# ADMIN ANALYTICS
# -------------------------

@app.route("/admin-data")
def admin_data():
    return jsonify(get_admin_analytics())


# -------------------------
# EXPORT LAST 30 DAYS CSV
# -------------------------

@app.route("/export-last-30-days")
def export_last_30_days():

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    records = list(
        predictions_collection.find(
            {"created_at": {"$gte": thirty_days_ago}}
        ).sort("created_at", -1)
    )

    if not records:
        return jsonify({"error": "No data found for last 30 days"}), 404

    file_path = "last_30_days_report.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "User",
            "Probability",
            "Risk",
            "Suggestion",
            "Created At"
        ])

        for r in records:
            writer.writerow([
                r.get("user", "N/A"),
                r.get("probability", 0),
                r.get("risk", "Unknown"),
                r.get("suggestion", "Not Available"),
                r.get("created_at").strftime("%Y-%m-%d %H:%M:%S")
                if r.get("created_at") else "N/A"
            ])

    return send_file(file_path, as_attachment=True)


# -------------------------
# BULK CSV PREDICTION (NO DB STORAGE)
# -------------------------

@app.route("/bulk-predict", methods=["POST"])
def bulk_predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    try:
        df = pd.read_csv(file)

        results = []
        total_probability = 0

        for index, row in df.iterrows():

            probability = calculate_churn_probability(
                float(row.get("tenure", 12)),
                float(row.get("watch_hours", 10)),
                float(row.get("days_since_login", 5)),
                row.get("subscription_type", "standard"),
                float(row.get("tickets_raised", 1)),
                float(row.get("profiles_used", 2))
            )

            risk = (
                "High" if probability > 0.7
                else "Medium" if probability > 0.4
                else "Low"
            )

            results.append({
                "user": row.get("email", f"User {index+1}"),
                "probability": probability,
                "risk": risk
            })

            total_probability += probability

        overall_probability = round(total_probability / len(results), 3)

        return jsonify({
            "results": results,
            "overall_probability": overall_probability
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
