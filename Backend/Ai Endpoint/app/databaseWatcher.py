import threading
import time
from pymongo import MongoClient
import certifi
from .traitement import process
from app.Service.PrefFetcher import get_temperature_pref
def translate_document(raw_doc):
    """
    Translate incoming MongoDB document format to internal format.
    
    Input format:
    {
        "_id": {...},
        "id": "room_name",
        "tempCapteur": float,
        "humiditeCapteur": float,
        "gazCapteur": float,
        "motion": {...},
        "porte": {...},
        "timestamp": str
    }
    
    Output format:
    {
        "id": "room_name",
        "tempCapteur": float,
        "humiditeCapteur": float,
        "doorCapteur": bool,
        "gazCapteur": float,
        "climatiseur": None,
        "temperaturePrefere": None,
        "timestamp": str
    }
    """
    try:
        # Validate required fields
        room_id = raw_doc.get("id")
        timestamp = raw_doc.get("timestamp")
        
        if not room_id:
            print(f"⚠️  Warning: Missing 'id' field in document")
            return None
            
        if not timestamp or not isinstance(timestamp, str):
            print(f"⚠️  Warning: Missing or invalid 'timestamp' field (must be string)")
            return None
        
        # Extract door sensor value safely
        porte_obj = raw_doc.get("porte")
        door_value = None
        if isinstance(porte_obj, dict):
            door_value = porte_obj.get("value")
        
        translated = {
            "id": room_id,
            "tempCapteur": raw_doc.get("tempCapteur", 0),
            "humiditeCapteur": raw_doc.get("humiditeCapteur", 0),
            "doorCapteur": door_value if door_value is not None else False,
            "gazCapteur": raw_doc.get("gazCapteur", 0),
            "climatiseur": None,
            "temperaturePrefere": get_temperature_pref(app=None, room_id=room_id),
            "timestamp": timestamp,
        }
        return translated
    except Exception as e:
        print(f"❌ Error translating document: {e}")
        return None

def watch_collection(app):
    with app.app_context():
        uri = app.config['MONGO_URI']
        db_name = app.config['DB_NAME']
        coll_name = app.config['COLLECTION_NAME']

    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client[db_name]
    collection = db[coll_name]

    print(f"watch  {coll_name}...")

    while True:
        try:
            with collection.watch([{'$match': {'operationType': 'insert'}}]) as stream:
                for change in stream:
                    raw_doc = change['fullDocument']
                    
                    # Translate document to internal format
                    translated_doc = translate_document(raw_doc)
                    
                    if translated_doc:
                        process(translated_doc)

        except Exception as e:
            print(f"error in database watcher ", e)
            time.sleep(3)

def start_watcher(app):
    thread = threading.Thread(target=watch_collection, args=(app,), daemon=True)
    thread.start()