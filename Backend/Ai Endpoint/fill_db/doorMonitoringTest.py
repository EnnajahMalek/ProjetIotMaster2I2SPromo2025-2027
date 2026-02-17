#satatic test to door opening anomalies
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import random
import time
from datetime import datetime, timezone

from ml.doorMonitoring.translator import IoTDataBridge
from ml.doorMonitoring.anomaly_detector import DoorAnomalyDetector


# ----------------------------
# STATIC TEST DATA GENERATOR
# ----------------------------
ROOMS = ["livingroom", "bedroom", "kitchen", "toilet"]


def generate_mock_data():
    now = datetime.now()

    # Randomize time instead of using current time
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    fake_time = now.replace(hour=random_hour, minute=random_minute)
    iso_time = fake_time.isoformat()

    return {
        "id": "livingroom",
        "doorCapteur": random.choice([True, False]),
        "light": random.choice([True, False]),  # IMPORTANT
        "timestamp": iso_time
    }


# ----------------------------
# DOOR MONITORING TEST
# ----------------------------
def run_door_monitoring():
    print(" Door Monitoring Simulator Started...\n")

    # Load model once (better performance)
    detector = DoorAnomalyDetector()
    detector.load_model("ml/doorMonitoring/models/door_anomaly.pkl")

    try:
        while True:
            data = generate_mock_data()

            # Translate to ML features
            ml_features = IoTDataBridge.translate(data)

            # Predict
            result = detector.predict(ml_features)
            """
            print("--------------------------------------------------")
            print(f"Room: {data['id']}")
            print(f"Door State: {data['doorCapteur']}")
            print(f"Time: {data['timestamp']}")
            print(f"AI Result: {result}")
            print("--------------------------------------------------\n")
            print(f"ml_features: {ml_features} | AI Result: {result}   ") 
            """
            print("ml_features:", ml_features, "| AI Result:", result)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Simulator Stopped.")


if __name__ == "__main__":
    run_door_monitoring()
