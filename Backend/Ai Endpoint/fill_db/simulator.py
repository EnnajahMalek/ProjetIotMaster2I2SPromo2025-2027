import time
import random
from datetime import datetime
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
from config import Config
#from ..app.Service.Sender import Sender

load_dotenv()

# Configuration
MONGO_URI =Config.MONGO_URI
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
            #send=Sender()
           
            mock_data = {
                "id": room ,                        
                "tempCapteur": round(random.uniform(18.0, 35.0), 1),
                "humiditeCapteur": random.randint(30, 70),
                "light": random.choice([True, False]),
                "doorCapteur": random.choice([True, False]),
                "gazCapteur": random.randint(0, 800) if room == "kitchen" else None,
                "climatiseur": random.choice([True, False]),
                "temperaturePrefere": 22,
                "timestamp": datetime.now().isoformat()
            }
            
            result = collection.insert_one(mock_data) 
            #send.send(mock_data)
            
            print(f" [SENT] Room: {mock_data['id']} | Temp: {mock_data['tempCapteur']}C | ID: {result.inserted_id}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n Simulator stopped")

if __name__ == "__main__":
    run_simulator()
