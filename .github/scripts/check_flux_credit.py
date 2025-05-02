import os
import requests
import json

print("📡 Starting credit check...")

url = "https://flux-ai.io/pricing/"
headers = {
    "Authorization": f"Bearer {os.getenv('FLUX_BEARER_TOKEN')}",
    "Content-Type": "application/json"
}

print(f"➡️ Sending POST request to {url}...")
res = requests.post(url, headers=headers)

print(f"🔁 Status Code: {res.status_code}")
print("📝 Raw response text:")
print(res.text)  # <--- This will help us debug

try:
    data = res.json()
    print(f"✅ JSON decoded: {data}")
except Exception as e:
    print(f"❌ Failed to decode JSON: {e}")
    exit(1)
