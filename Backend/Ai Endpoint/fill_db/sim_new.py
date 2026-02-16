import time
import random
from datetime import datetime, timezone
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

load_dotenv()

# Configuration
MONGO_URI = "mongodb+srv://projetiot:PigZNQGf6lPy97Pk@projetiot.mwwvunz.mongodb.net/"
DB_NAME = "Testing"
COLLECTION_NAME = "sensor_logs"

# List of rooms to rotate through
ROOMS = ["livingroom", "bedroom", "kitchen", "toilet"]

def run_simulator():
    
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    print(f" Simulation started on {DB_NAME}.{COLLECTION_NAME}")
    try:
        while True:
            room = random.choice(ROOMS)
            current_time = datetime.now(timezone.utc).isoformat()
            
            mock_data = {
                "id": room,
                "tempCapteur": round(random.uniform(18.0, 35.0), 2),
                "humiditeCapteur": round(random.uniform(30.0, 70.0), 2),
                "gazCapteur": round(random.uniform(0.0, 900.0), 2) if room == "kitchen" else round(random.uniform(0.0, 100.0), 2),
                "motion": {
                    "sensor_id": "001",
                    "sensor_type": "motion",
                    "value": random.choice([True, False]),
                    "timestamp": current_time
                },
                "porte": {
                    "sensor_id": "001-porte",
                    "sensor_type": "porte",
                    "value": random.choice([True, False]),
                    "timestamp": current_time
                },
                "timestamp": current_time
            }
            
            result = collection.insert_one(mock_data)
            print(f" [SENT] Room: {mock_data['id']} | Temp: {mock_data['tempCapteur']}C | Motion: {mock_data['motion']['value']} | ID: {result.inserted_id}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n Simulator stopped")
    finally:
        client.close()

if __name__ == "__main__":
    run_simulator()