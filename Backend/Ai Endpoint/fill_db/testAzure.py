import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/device/send"

payload = {
  "topic": "home-alerts",
  "title": "Gas Leak Detected",
  "timestamp": "2026-02-12T14:30:00Z",
  "alert": {
    "is_anomaly": True,
    "description": "High concentration of gas detected in the kitchen",
    "type": "Gaz",
    "severity": "HIGH"
  }
}


headers = {
    "Content-Type": "application/json"
}



response = requests.post(url, data=json.dumps(payload), headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

