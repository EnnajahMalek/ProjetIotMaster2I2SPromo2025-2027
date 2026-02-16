import sys
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

load_dotenv()

class Sender:
    def __init__(self):
        self.url = "https://backendiotproject-c4gbdtdqcebjb9c9.spaincentral-01.azurewebsites.net/api/device/send"
        self.headers = {
            "Content-Type": "application/json"
        }

    def send(self, data):
        """
        Takes a dictionary (data), converts it to JSON, and POSTs it.
        """
        try:
            # Send the request
            # Note: requests.post(json=data) automatically handles json.dumps and headers
            response = requests.post(
                self.url, 
                json=data, 
                headers=self.headers
            )
            print(data)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                print("Data sent successfully to Azure.")
            else:
                print(f" Error: {response.text}")
                
            return response
            
        except Exception as e:
            print(f" Connection Error: {e}")
            return None

