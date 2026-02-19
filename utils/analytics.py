from datetime import datetime, timedelta
from utils.db import users_collection, predictions_collection


def get_admin_analytics():

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # -------------------------
    # TOTAL USERS
    # -------------------------
    total_users = users_collection.count_documents({})

    # -------------------------
    # TOTAL PREDICTIONS
    # -------------------------
    total_predictions = predictions_collection.count_documents({})

    # -------------------------
    # LAST 30 DAYS USERS
    # -------------------------
    last_30_days_users = predictions_collection.distinct(
        "user",
        {"created_at": {"$gte": thirty_days_ago}}
    )

    # -------------------------
    # OVERALL PROBABILITY
    # -------------------------
    all_predictions = list(
        predictions_collection.find({}, {"probability": 1})
    )

    if all_predictions:
        overall = sum(p.get("probability", 0) for p in all_predictions) / len(all_predictions)
    else:
        overall = 0

    # -------------------------
    # HISTORY (Last 50)
    # -------------------------
    history_records = list(
        predictions_collection
        .find({})
        .sort("created_at", -1)
        .limit(50)
    )

    formatted_history = []

    for r in history_records:
        formatted_history.append({
            "user": r.get("user", "N/A"),
            "probability": r.get("probability", 0),
            "risk": r.get("risk", "Unknown"),
            "suggestion": r.get("suggestion", "N/A"),
            "created_at": r["created_at"].isoformat()
            if r.get("created_at") else ""
        })

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "last_30_days_users_count": len(last_30_days_users),
        "overall": overall,
        "history": formatted_history
    }
