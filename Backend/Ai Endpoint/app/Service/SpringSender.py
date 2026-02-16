import json 
import time 
import requests
import hmac
import hashlib


class SpringBootClient:
    def __init__(self, base_url, device_id, device_token, shared_secret):
        self.base_url = base_url
        self.device_id = device_id
        self.device_token = device_token  # ✅ No encoding
        self.shared_secret = shared_secret
    
    def send_notification(self, topic, title, body):  # ✅ Better method name
        timestamp = str(int(time.time()))
        data = {
            "topic": topic,
            "title": title,
            "body": body
        }
        body_str = json.dumps(data)
        signature = self._generate_signature(timestamp, body_str)
        
        headers = {
            'Content-Type': 'application/json',
            'X-Device-ID': self.device_id,
            'X-Device-Token': self.device_token,
            'X-Timestamp': timestamp,
            'X-Signature': signature   
        }
        
        # DEBUG: Print what we're sending
        print(f"[DEBUG] Timestamp: {timestamp}")
        print(f"[DEBUG] Body: {body_str}")
        print(f"[DEBUG] Signature: {signature}")
        print(f"[DEBUG] Headers: {headers}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/device/send",  # ✅ Correct endpoint
                headers=headers,
                data=body_str,
                timeout=30
            )
            print(f"[DEBUG] Response Status: {response.status_code}")
            print(f"[DEBUG] Response Body: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending to Spring Boot: {e}")
            raise

    def _generate_signature(self, timestamp, body):
        message = f"{timestamp}{body}".encode('utf-8')
        signature = hmac.new(
            self.shared_secret.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        return signature


spring_client = SpringBootClient(
    base_url='http://172.26.80.172:8080',  # Use your server IP here
    device_id='flask-server',
    device_token=r"""PU32X7L@.'Q}t,tBV)z]0.3"Mkk0x0b:2ccHY0(qk(@#@#R@v-EK-K@pLi[PSwuk[[{LTr)Eze@}G{iX2x6TS2]p"8)qc=W(Q20R\.066';Mb.E8EX;RLWMciD""",
    shared_secret=r"""x.9xXe+t7LvolRG.Gwz3jwm[,8\j2PRdHFUpJI4'"ux4Y1},\tcc\eum2kPlp[s.L@}{u2I9ZBr"hr!0s0.=7w@#cQG-?1A:*JEf|zO8wwe@pyBKk69p79f"""
)

# Usage:
result = spring_client.send_notification(
    topic="sensor-alerts",
    title="Temperature Alert", 
    body="Temperature exceeded threshold"
)