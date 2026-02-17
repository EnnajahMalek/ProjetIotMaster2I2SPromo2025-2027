import datetime
import pandas as pd
import numpy as np
from pymongo import MongoClient
import certifi
from config import Config

# MongoDB config
MONGO_URI =Config.MONGO_URI
DB_NAME = "Testing"
COLLECTION_NAME = "Room-Agents"
ROOMS = ["livingroom", "bedroom", "kitchen", "toilet"]

class IoTDataBridge:
    """
    The Bridge: Translates Raw Project JSON to ML-Ready Features.
    """
    
    @staticmethod
    def fetch_latest_light_states():
        """
        Fetch the latest light states for all rooms from MongoDB.
        """
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        latest_states = {}
        for room in ROOMS:
            doc = collection.find({"id": room}).sort("timestamp", -1).limit(1)
            latest = list(doc)
            if latest:
                latest_states[room] = latest[0].get("light", False)
            else:
                latest_states[room] = False
        client.close()
        return latest_states
    
    @staticmethod
    def translate(raw_json):
        """
        Converts the project JSON structure:
        { "id": "livingroom", "light": bool, "doorCapteur": bool, "timestamp": str }
        Into the format the ML Model expects.
        """
        try:
            # 1. Parse the ISO Timestamp
            dt = datetime.datetime.fromisoformat(raw_json["timestamp"])
            
            # 2. Extract Time-based features
            hour = dt.hour
            day_of_week = dt.weekday()
            is_weekend = day_of_week >= 5
            is_night = (hour >= 22 or hour <= 6)
            
            # 3. Map Sensor names
            door_open = bool(raw_json.get("doorCapteur", False))
            current_room_light = bool(raw_json.get("light", False))
            current_room = raw_json["id"]
            
            # 4. Fetch latest light states from other rooms
            latest_states = IoTDataBridge.fetch_latest_light_states()
            
            # Override current room's light
            latest_states[current_room] = current_room_light
            
            # 5. Build feature variables
            bedroom_light = latest_states.get("bedroom", False)
            kitchen_light = latest_states.get("kitchen", False)
            toilet_light = latest_states.get("toilet", False)
            livingroom_light = latest_states.get("livingroom", False)
            
            other_rooms_on = sum([v for k, v in latest_states.items() if k != current_room])
            any_light_on = any(latest_states.values())
            
            # 6. Build the ML-ready payload
            ml_ready_payload = {
                "hour": hour,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "is_night": is_night,
                "door_open": door_open,
                "livingroom_light": livingroom_light,
                "bedroom_light": bedroom_light,
                "kitchen_light": kitchen_light,
                "toilet_light": toilet_light,
                "other_rooms_lights_on": other_rooms_on,
                "any_light_on": any_light_on
            }
            
            return ml_ready_payload
            
        except Exception as e:
            print(f" Translation Error: {e}")
            return None
