import requests

#url = "http://10.60.16.201:8080/api/notifications/send"
url = "http://172.26.80.172:8080/api/device/send"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}
data = {
    "topic": "23dcc",
    "title": "wtssp ",
    "body": " from Python",
 
     }

response = requests.post(url, json=data)


print("Status:", response.status_code)
print("Response:", response.text)
