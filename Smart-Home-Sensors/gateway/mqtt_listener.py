import paho.mqtt.client as mqtt
from datetime import datetime, timezone , timedelta
import json
from db_handler import collectionData

current_time = datetime.now(timezone.utc)

def on_message(client, userdata, msg):
    global current_time
    try:
        data = json.loads(msg.payload.decode())
        result = collectionData.insert_one({
            **data,
            "timestamp": current_time
        })
        current_time += timedelta(minutes=5)
        print(f"✓ Inserted successfully with ID: {result.inserted_id}")
    except json.JSONDecodeError as e:
        print(f"✗ JSON decode error: {e}")
    except Exception as e:
        print(f"✗ Insert failed: {e}")

client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883)


client.subscribe("home/+")    


client.loop_forever()
