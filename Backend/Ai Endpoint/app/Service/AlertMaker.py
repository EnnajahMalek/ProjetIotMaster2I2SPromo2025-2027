import json
from datetime import datetime
import numpy as np

class AlertMaker:
    unit = {}
    unit["Gaz"] = "PPM"
    unit["Fire"] = "°C"
    """
    Standardizes ML and Rule results into a unified JSON format 
    for the secondary backend.
    """
    
    def __init__(self):
        self.topic ="home-alerts"

    def _convert_to_native(self, obj):
        """
        Recursively converts numpy types and other non-JSON-serializable objects
        to Python native types that can be serialized to JSON.
        """
        if isinstance(obj, dict):
            return {key: self._convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_native(item) for item in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    def create_alert(self, sensor_id, result, alert_type,time,value):
       
        
        # 1. Determine if it's an anomaly (Handles both 'is_fire' and 'is_anomaly' keys)
        is_anomaly = result.get('is_fire', result.get('is_anomaly', False))
        
        # 2. Extract description from triggers if they exist
        description = self._generate_description(sensor_id, result, alert_type,value )
        
        # 3. Build the payload
        payload = {
            "topic": self.topic,
            "title": f"{alert_type} Alert: {sensor_id.capitalize()}",
            "timestamp": time if time else datetime.utcnow().isoformat(),
            "alert": {
                "is_anomaly": is_anomaly,
                "description": description,
                "type": alert_type,
                "severity": result.get('severity', 'NORMAL'),
                "roomId" : sensor_id
            }
        }
        
        # Convert all numpy types to native Python types for JSON serialization
        payload = self._convert_to_native(payload)
        
        return payload

    def _generate_description(self, sensor_id, result, alert_type,value):
            if alert_type == "Climatiseur":
                if value ==0:
                    return f"✅ AC Update: {sensor_id} has reached target temperature."
                else:
                 return f"❄️ AC Alert: {sensor_id} is {value}°C (Above target). Adjusting now."
            elif alert_type == "Door":
                if result.get('is_anomaly', False):
                    return f"⚠️ Security: Front Door opened at an unusual time! "
                else:
                    return f"🏠 Door in {sensor_id} is open (Routine activity detected)."  
            elif alert_type == "Light":
                if result.get('is_anomaly', False):
                    return f"💡 Energy Alert: Toilet light left on for {value} seconds. Please turn it off."
                else:
                    return f"✅ Light in {sensor_id} is off."      
            elif alert_type == "Gaz":
                      return f"🚨 DANGER: High Gaz levels ({value} ppm) in {sensor_id}! Check immediately."
    
            elif alert_type == "Fire":
               if result.get('is_fire', False):
                    return f"🔥 FIRE ALERT: High Risk in {sensor_id}! Severity: {result.get('severity','meduim')}."
               else: 
                  return f"✅ Fire safety check: {sensor_id} is normal ({value}°C)."
  
            

    