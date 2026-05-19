from pymongo import MongoClient
import os

client = MongoClient(
    os.environ.get("MONGO_URI"),
    serverSelectionTimeoutMS=5000
)

db = client["churnDB"]

users_collection = db["users"]
predictions_collection = db["predictions"]