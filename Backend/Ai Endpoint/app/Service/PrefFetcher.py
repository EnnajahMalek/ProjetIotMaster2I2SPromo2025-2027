from pymongo import MongoClient
import certifi



def get_temperature_pref(app, room_id):
    """
    Fetch temperature preference for a specific room from Room-Agents collection.
    
    :param app: Flask app instance
    :param room_id: The id field of the room (e.g., "toilet")
    :return: temperature preference value or None
    """

    # Get config safely inside app context
    with app.app_context():
        uri = app.config['MONGO_URI']
        db_name = app.config['DB_NAME']

    # Connect to MongoDB
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client[db_name]
    collection = db["Room-Agents"]  

    # Find the document
    room = collection.find_one({"id": room_id})

    if room and "temperaturepref" in room:
        return room["temperaturepref"]

    return None
