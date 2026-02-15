import os
from pymongo import MongoClient

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")

if not mongo_uri:
    raise RuntimeError("Missing MONGODB_URI environment variable.")

client = MongoClient(mongo_uri)

db = client["Testing"] 
collectionData = db["sensor_logs"] 
collectionAgent = db["Room-Agents"]


