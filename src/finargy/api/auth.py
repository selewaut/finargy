import http.client
import json

conn = http.client.HTTPSConnection("api.iolinversiones.com")

import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

payload = json.dumps({
  "grant_type": "password",
  "username": username,
  "password": password,
  "refresh_token": ""
})
headers = {
  "Content-Type": "application/json"
}

conn.request(
    "POST",
    "/auth/token",
    body=payload,
    headers=headers,
)

response = conn.getresponse()
print(response.read().decode())

conn.close()