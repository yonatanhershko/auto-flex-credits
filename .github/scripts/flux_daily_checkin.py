import os
import re
import json
import requests

print("🔹 📡 Starting Flux AI daily credit check-in...")
print("🔹 📡 Checking credits via /pricing...")

# Get your token from the environment variable
token = os.getenv("FLUX_TOKEN")
if not token:
    print("❌ FLUX_TOKEN not found in environment variables.")
    exit(1)

headers = {
    "Authorization": token,  # should include 'Bearer ...'
    "Accept": "text/x-component",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.post("https://flux-ai.io/pricing/", headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed: Unexpected status code: {response.status_code}")
        print("📦 Response:", response.text[:300])
        exit(1)

    # RSC-style response: look for line starting with 1: and extract JSON
    matches = re.findall(r'\n1:(\{.*?\})', response.text)

    if not matches:
        print("❌ No valid JSON found in /pricing response.")
        print("📦 Raw response (start):", response.text[:300])
        exit(1)

    json_data = json.loads(matches[0])
    credits = json_data["data"].get("credits", "N/A")

    print(f"✅ You currently have {credits} credits.")

except Exception as e:
    print("❌ Failed to decode structured credit info.")
    print("🔍 Error:", e)
    exit(1)
