import datetime
import pandas as pd
import numpy as np

class IoTDataBridge:
    """
    The Bridge: Translates Raw Project JSON to ML-Ready Features.
    """
    
    @staticmethod
    def translate(raw_json):
        """
        Converts the project JSON structure:
        { "id": "livingroom", "light": bool, "doorCapteur": bool, "timestamp": str }
        Into the format the ML Model expects.
        """
        try:
            # 1. Parse the ISO Timestamp
            # Converts "2026-02-08T23:05:58..." into a Python datetime object
            dt = datetime.datetime.fromisoformat(raw_json["timestamp"])
            
            # 2. Extract Time-based features
            hour = dt.hour
            day_of_week = dt.weekday()
            is_weekend = day_of_week >= 5
            # Defining 'night' as 10 PM to 6 AM
            is_night = (hour >= 22 or hour <= 6)
            
            # 3. Map Sensor names
            # Project: doorCapteur -> ML: door_open
            # Project: light -> ML: livingroom_light
            door_open = bool(raw_json.get("doorCapteur", False))
            living_light = bool(raw_json.get("light", False))
            
            # 4. Handle context (Other rooms)
            # Since your current JSON only sends 'livingroom', we assume others are off
            # or you can extend this if you add 'bedroom' data later.
            bedroom_light = False
            kitchen_light = False
            toilet_light = False
            
            other_rooms_on = sum([bedroom_light, kitchen_light, toilet_light])
            any_light_on = any([living_light, bedroom_light, kitchen_light, toilet_light])
            
            # 5. Build the exact dictionary the Model Class expects
            # Order doesn't matter here; the Detector class will sort it into a Matrix.
            ml_ready_payload = {
                "hour": hour,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "is_night": is_night,
                "door_open": door_open,
                "livingroom_light": living_light,
                "bedroom_light": bedroom_light,
                "kitchen_light": kitchen_light,
                "toilet_light": toilet_light,
                "other_rooms_lights_on": other_rooms_on,
                "any_light_on": any_light_on
            }
            
            return ml_ready_payload
            
        except Exception as e:
            print(f"❌ Translation Error: {e}")
            return None