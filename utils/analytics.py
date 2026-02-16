from datetime import datetime, timedelta
from utils.db import users_collection, predictions_collection


def get_admin_analytics():

    total_predictions = predictions_collection.count_documents({})
    total_users = users_collection.count_documents({})

    records = list(
        predictions_collection
        .find({})
        .sort("created_at", -1)
        .limit(50)
    )

    # Overall probability
    probabilities = [r.get("probability", 0) for r in records]
    overall = round(sum(probabilities) / len(probabilities), 3) if probabilities else 0

    # Last 30 days users
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_users = predictions_collection.distinct(
        "user",
        {"created_at": {"$gte": thirty_days_ago}}
    )

    # Risk counts
    high_risk = predictions_collection.count_documents({"risk": "High"})
    medium_risk = predictions_collection.count_documents({"risk": "Medium"})
    low_risk = predictions_collection.count_documents({"risk": "Low"})

    formatted_history = []
    for r in records:
        formatted_history.append({
            "_id": str(r["_id"]),
            "user": r.get("user"),
            "probability": r.get("probability"),
            "risk": r.get("risk"),
            "suggestion": r.get("suggestion"),
            "created_at": r.get("created_at").isoformat() if r.get("created_at") else None
        })

    return {
        "history": formatted_history,
        "overall": overall,
        "total_users": total_users,
        "total_predictions": total_predictions,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "last_30_days_users_count": len(recent_users)
    }
