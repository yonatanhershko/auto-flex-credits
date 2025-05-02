import requests
import os
import json

TOKEN = os.getenv("FLUX_TOKEN")

def log(message):
    print(f"🔹 {message}")

def check_credits():
    log("📡 Checking credits via /pricing...")
    url = "https://flux-ai.io/pricing/"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "text/x-component",
    }

    try:
        response = requests.post(url, headers=headers, json={"site": "flux-ai.io"})
        log(f"🔁 Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"📦 Response text: {response.text}")
            return

        # Handle non-JSON responses (e.g., HTML errors)
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            print(f"❌ Failed to decode JSON: {response.text[:300]}...")
            return

        code = json_data.get("code")
        if code != 200:
            print(f"❌ Error code: {code} — {json_data.get('msg')}")
            return

        user_data = json_data.get("data", {})
        credits = user_data.get("credits")
        email = user_data.get("email")
        name = user_data.get("nickName")

        log(f"✅ Success: {credits} credits left for {name} ({email})")

    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    log("📡 Starting Flux AI daily credit check-in...")
    check_credits()
