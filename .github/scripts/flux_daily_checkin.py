import os
import requests

SIGNIN_URL = 'https://api2.tap4.ai/signIn'
HEADERS = {
    'Authorization': f"Bearer {os.getenv('FLUX_TOKEN')}",
    'Content-Type': 'application/json',
    'Accept': '*/*'
}
PAYLOAD = {'site': 'flux-ai.io'}

print("🔹 📡 Starting Flux AI daily credit check-in...")

try:
    response = requests.post(SIGNIN_URL, json=PAYLOAD, headers=HEADERS)
    print(f"🔹 HTTP {response.status_code}")
    
    # Attempt to parse JSON
    try:
        data = response.json()
    except ValueError:
        print("❌ Failed to decode JSON.")
        print("📦 Raw response (start):", response.text[:500])
        exit(1)

    if data.get("code") == 200:
        print("✅ Check-in successful!")
    elif data.get("msg", "").lower().startswith("checked in today"):
        print("✅ Already checked in today.")
    else:
        print(f"⚠️ Unexpected response: {data}")
        exit(1)

except Exception as e:
    print(f"❌ Exception occurred: {e}")
    exit(1)
