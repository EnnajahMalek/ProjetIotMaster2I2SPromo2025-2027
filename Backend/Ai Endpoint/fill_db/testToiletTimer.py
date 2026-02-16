from pymongo import MongoClient
from datetime import datetime

# Setup Connection
MONGO_URI = "mongodb+srv://projetiot:PigZNQGf6lPy97Pk@projetiot.mwwvunz.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["Testing"]
collection = db["sensor_logs"]

# --- SCENARIOS ---
data_to_push = [
    # 1. THE NORMAL CASE (Evening, home, lights on, door closed)
    {
        "id": "toilet",
        "tempCapteur": 24.5,
        "humiditeCapteur": 45,
        "light": False,
        "doorCapteur": True,
        "gazCapteur": None,
        "climatiseur": True,
        "temperaturePrefere": 22,
        "timestamp": "2026-02-10T20:30:00.000000" # 8:30 PM
    },
    
    # 2. ANOMALY 1: The "Midnight Intruder" (Late night, lights off, door open)
    {
        "id": "toilet",
        "tempCapteur": 20.1,
        "humiditeCapteur": 50,
        "light": True,
        "doorCapteur": False, # ← 
        "gazCapteur": None,
        "climatiseur": False,
        "temperaturePrefere": 22,
        "timestamp": "2026-02-10T20:31:00.000000" # 3:15 AM
    },
    
    # 3. ANOMALY 2: The "Ghost" (Working hours, door open, no one home)
    {
        "id": "toilet",
        "tempCapteur": 22.0,
        "humiditeCapteur": 48,
        "light": True,
        "doorCapteur": True, # ← 
        "gazCapteur": None,
        "climatiseur": False,
        "temperaturePrefere": 22,
        "timestamp": "2026-02-10T20:38:00.000000" 
    },
    
    # 4. ANOMALY 3: The "Forgot Door" (Sleeping hours, door open)
    {
        "id": "toilet",
        "tempCapteur": 19.5,
        "humiditeCapteur": 55,
        "light": False,
        "doorCapteur": True, # ← ALERT
        "gazCapteur": None,
        "climatiseur": False,
        "temperaturePrefere": 22,
        "timestamp": "2026-02-10T23:50:00.000000" # 11:50 PM
    }
]

# Push to MongoDB
result = collection.insert_many(data_to_push)
print(f"Successfully pushed {len(result.inserted_ids)} scenarios to MongoDB!")