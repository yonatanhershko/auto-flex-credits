# .github/scripts/flux_daily_checkin.py

import requests
import datetime
import os

def checkin():
    token = os.getenv("FLUX_BEARER_TOKEN")
    if not token:
        print("❌ Missing FLUX_BEARER_TOKEN environment variable.")
        exit(1)

    url = "https://flux-ai.io/pricing"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(url, headers=headers)
        res.raise_for_status()
        data = res.json()

        credits = data["data"].get("credits", "Unknown")
        timestamp = data["data"].get("signInTime")
        date_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        print("✅ Check-in successful!")
        print(f"🪙 Credits: {credits}")
        print(f"📅 Sign-in time: {date_str}")

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", str(e))
        if res is not None:
            print("📦 Response text:", res.text)
        exit(1)

if __name__ == "__main__":
    checkin()
