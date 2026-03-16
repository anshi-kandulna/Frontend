import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
#print(f"Connecting to MongoDB at: {MONGO_URI}")

client = MongoClient(MONGO_URI)

# Main database
db = client["patient"]
