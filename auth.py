import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.iolinversiones.com"

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

token_response = requests.post(
    f"{BASE_URL}/auth/token",
    json={
        "grant_type": "password",
        "username": username,
        "password": password,
        "refresh_token": "",
    },
    headers={"Content-Type": "application/json"},
)
token_response.raise_for_status()
access_token = token_response.json()["data"]["access_token"]

end = date.today()
start = end - timedelta(days=7)

history_response = requests.get(
    f"{BASE_URL}/broker/accounts/AR/portfolio/history",
    headers={"Authorization": f"Bearer {access_token}"},
    params={
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    },
)
if not history_response.ok:
    try:
        error = history_response.json().get("error")
    except ValueError:
        error = history_response.text
    print(f"HTTP {history_response.status_code}: {error}")
    history_response.raise_for_status()

payload = history_response.json()
data = payload.get("data", payload)
history = data.get("history", data) if isinstance(data, dict) else data

df = pd.json_normalize(history)

output_path = Path("data/portfolio/portfolio_history.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
