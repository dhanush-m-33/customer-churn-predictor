from datetime import datetime
from utils.db import users_collection


def register_user(data):
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return {"success": False, "error": "Email and password required"}

    # Prevent admin registration
    if email == "admin@churn.com":
        return {"success": False, "error": "Admin account cannot be registered"}

    if users_collection.find_one({"email": email}):
        return {"success": False, "error": "User already exists"}

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "role": "user",
        "created_at": datetime.utcnow()
    })

    return {"success": True}


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    # Hardcoded Admin
    if email == "admin@churn.com" and password == "admin123":
        return {
            "success": True,
            "role": "admin",
            "email": email
        }

    user = users_collection.find_one({
        "email": email,
        "password": password
    })

    if not user:
        return {"success": False, "error": "Invalid credentials"}

    return {
        "success": True,
        "role": "user",
        "email": user["email"]
    }
