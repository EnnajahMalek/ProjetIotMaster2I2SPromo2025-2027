from sensors.temperateur_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gaz_sensor import GasSensor
from sensors.anomalous import anomalous
from gateway.db_handler import collectionAgent
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime, timezone

client = mqtt.Client()
client.connect("localhost", 1883)

def read_sensor_data(room_name):
    humidity = HumiditySensor()
    temperature = TemperatureSensor()
    gaz = GasSensor()
    climat_staus = collectionAgent.find_one(
        {"id": room_name},
        {"clima": 1, "_id": 0}
    )
    if climat_staus['clima']:
        temperature.ac_on(True)
    window_status = collectionAgent.find_one(
        {"id": room_name},
        {"window":1, "_id":0}
    )
    if window_status['window']:
        gaz.trigger_leak(False)
    return {
        "id": room_name,
        "tempCapteur": temperature.read_value(),
        "humiditeCapteur": humidity.read_value(),
        "gazCapteur": gaz.read_value(),
    }
def create_room_data(sensor_id, room_name):
    return {
        **read_sensor_data(room_name),
        "motion": {
            "sensor_id": sensor_id,
            "sensor_type": "motion",
            "value": anomalous(False,60,True),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "porte": {
            "sensor_id": f"{sensor_id}-porte",
            "sensor_type": "porte",
            "value": anomalous(False, 60, True),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
rooms = [
    {"id": "001", "name": "livingroom"},
    {"id": "002", "name": "kitchen"},
    {"id": "003", "name": "bedroom"},
    {"id": "004", "name": "toilet"}
]
while True:  
    for room in rooms:
        room_data = create_room_data(room["id"], room["name"])
        
        if not room_data.get("id") or room_data.get("tempCapteur") is None:
            print(f"Invalid data for {room['name']}: missing required fields")
            continue
        
        result = client.publish(f"home/{room['name']}", json.dumps(room_data))
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✓ Data sent successfully to home/{room['name']}")
            print(f"  Room: {room_data['id']} | Temp: {room_data['tempCapteur']}°C | Humidity: {room_data['humiditeCapteur']}%")
        else:
            print(f"✗ Failed to send data to home/{room['name']} (code: {result.rc})")
        
        time.sleep(5)
