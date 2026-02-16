from pymongo import MongoClient
from datetime import datetime






class MovementDetector:
    MONGO_URI = "mongodb+srv://projetiot:PigZNQGf6lPy97Pk@projetiot.mwwvunz.mongodb.net/"
    DB_NAME = "Testing"
    COLLECTION_NAME = "sensor_logs" 
    def __init__(self,mongo_uri= MONGO_URI, db_name="Testing", collection_name="motion"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def detect_movement(self):
        """Check if movement is detected from MongoDB"""
        try:
            motion_data = self.collection.find_one(sort=[("_id", -1)])
            if motion_data and motion_data.get("motion", {}).get("value"):
                return True
            return False
        except Exception as e:
            print(f"Error detecting movement: {e}")
            return False
    
    def log_movement(self, status):
        """Log movement event to MongoDB"""
        try:
            self.collection.insert_one({
                "timestamp": datetime.utcnow(),
                "motion": {"value": status}
            })
        except Exception as e:
            print(f"Error logging movement: {e}")
    
    def get_latest_movement(self):
        """Get latest movement data"""
        try:
            return self.collection.find_one(sort=[("_id", -1)])
        except Exception as e:
            print(f"Error fetching movement data: {e}")
            return None
    
    