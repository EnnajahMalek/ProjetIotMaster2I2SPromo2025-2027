from pymongo import MongoClient
from datetime import datetime, timedelta

# Setup Connection
MONGO_URI = "mongodb+srv://projetiot:PigZNQGf6lPy97Pk@projetiot.mwwvunz.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["Testing"]
collection = db["sensor_logs"]

# Get current time for relative timestamps
now = datetime.now()

# --- FIRE DETECTION SCENARIOS ---
# Gas levels in PPM (parts per million):
# Normal: 50-100 ppm, Safe cooking: 100-300 ppm, Anomaly: 301-600 ppm, Critical: 601+ ppm
data_to_push = [
    # 1. THE NORMAL CASE (Baseline stable environment)
    {
        "id": "kitchen",
        "tempCapteur": 22.0,
        "humiditeCapteur": 45,
        "gazCapteur": 75,       # ppm - baseline normal
        "light": False,
        "doorCapteur": False,
        "timestamp": (now - timedelta(minutes=15)).isoformat()
    },
    
    # 2. NORMAL ACTIVITY (Cooking: Moderate temp rise, moderate gas, high humidity)
    # This should be seen as "Normal" or "Low" by a well-trained ML model
    {
        "id": "kitchen",
        "tempCapteur": 29.5,
        "humiditeCapteur": 65, # Steam from cooking
        "gazCapteur": 200,      # ppm - normal cooking range
        "light": True,
        "doorCapteur": False,
        "timestamp": (now - timedelta(minutes=10)).isoformat()
    },
    
    # 3. ANOMALY: SMOLDERING FIRE (Slow temp rise, dry air, NO gas)
    # The ML should catch this because Humidity is DROPPING while Temp is RISING
    {
        "id": "kitchen",
        "tempCapteur": 38.0,
        "humiditeCapteur": 25, # Air getting very dry
        "gazCapteur": 50,       # ppm - minimal
        "light": False,
        "doorCapteur": False,
        "timestamp": (now - timedelta(minutes=5)).isoformat()
    },
    
    # 4. CRITICAL ANOMALY: GAS FIRE (Explosive temp, explosive gas, extremely dry)
    # This should trigger "CRITICAL" severity
    {
        "id": "kitchen",
        "tempCapteur": 65.0,  # Extreme heat
        "humiditeCapteur": 12,  # Extreme dry
        "gazCapteur": 1000,     # ppm - critically high (fire hazard)
        "light": False,
        "doorCapteur": False,
        "timestamp": now.isoformat()
    }
]

# Push to MongoDB
try:
    result = collection.insert_many(data_to_push)
    print(f" Successfully pushed {len(result.inserted_ids)} fire scenarios to MongoDB!")
    print("Check your service console to see if the ML flagged the anomalies.")
except Exception as e:
    print(f" Error pushing to MongoDB: {e}")