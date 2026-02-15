from sensors.temperateur_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gaz_sensor import GasSensor
from sensors.anomalous import anomalous
from gateway.db_handler import collectionAgent
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime, timezone,timedelta
import threading

client = mqtt.Client()
client.connect("localhost", 1883)


def read_sensor_data(room_name, temperature, humidity, gaz):
    climat_staus = collectionAgent.find_one(                         
        {"id": room_name},
        {"clima": 1, "_id": 0}
    )
    if climat_staus:
        temperature.toggle_ac(climat_staus.get("clima"))
    
    window_status = collectionAgent.find_one(
        {"id": room_name},
        {"window": 1, "_id": 0}
    )
    if window_status:
        gaz.trigger_leak(not window_status.get('window'))
    
    return {
        "id": room_name,
        "tempCapteur": temperature.read_value(),
        "humiditeCapteur": humidity.read_value(),
        "gazCapteur": gaz.read_value(),
    }

def create_room_data(sensor_id, room_name, temperature, humidity, gaz,current_time):
    """Create room data with sensor readings"""
    return {
        **read_sensor_data(room_name, temperature, humidity, gaz),
        "motion": {
            "sensor_id": sensor_id,
            "sensor_type": "motion",
            "value": anomalous(False, 60, True),
            "timestamp":current_time.isoformat(),
        },
        "porte": {
            "sensor_id": f"{sensor_id}-porte",
            "sensor_type": "porte",
            "value": anomalous(False, 60, True),
            "timestamp":current_time.isoformat(),
        },
    }

def publish_room_data(room):
    """Thread function to publish data for a single room"""
    temperature = TemperatureSensor()
    humidity = HumiditySensor()
    gaz = GasSensor()
    current_time = datetime.now(timezone.utc)
    while True:
        room_data = create_room_data(room["id"], room["name"], temperature, humidity, gaz,current_time)
        current_time += timedelta(minutes=5)
        if not room_data.get("id") or room_data.get("tempCapteur") is None:
            print(f"Invalid data for {room['name']}: missing required fields")
            time.sleep(1)
            continue
        
        result = client.publish(f"home/{room['name']}", json.dumps(room_data))
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✓ {room['name']}: Temp: {room_data['tempCapteur']}°C | Humidity: {room_data['humiditeCapteur']}%")
        else:
            print(f"✗ Failed to send data to home/{room['name']} (code: {result.rc})")
        
        time.sleep(1)

rooms = [
    {"id": "001", "name": "livingroom"},
    {"id": "002", "name": "kitchen"},
    {"id": "003", "name": "bedroom"},
    {"id": "004", "name": "toilet"}
]


threads = []
for room in rooms:
    thread = threading.Thread(target=publish_room_data, args=(room,), daemon=True)
    thread.start()
    threads.append(thread)
    print(f"Started thread for {room['name']}")


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")


