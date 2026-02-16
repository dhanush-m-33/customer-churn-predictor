from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dhanush8305_db_user:x0hvG4l9GbMlUKOk@churndb.rvyx6h1.mongodb.net/?retryWrites=true&w=majority",
    serverSelectionTimeoutMS=5000
)

db = client["churnDB"]

users_collection = db["users"]
predictions_collection = db["predictions"]
