import paho.mqtt.client as mqtt
from datetime import datetime, timezone
import json
from db_handler import collectionData,collectionAgent

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        result = collectionData.insert_one({
            **data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
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
