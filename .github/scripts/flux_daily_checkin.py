import os
import requests

SIGNIN_URL = "https://api2.tap4.ai/signIn"
PRICING_URL = "https://flux-ai.io/pricing/"

def log(msg):
    print(f"🔹 {msg}")

def main():
    log("📡 Starting Flux AI daily credit check-in...")

    token = os.getenv("FLUX_TOKEN")
    if not token:
        print("❌ FLUX_TOKEN environment variable not set.")
        exit(1)

    log("🔐 Signing in to get new access token...")
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json",
    }
    payload = {"site": "flux-ai.io"}

    signin_resp = requests.post(SIGNIN_URL, json=payload, headers=headers)
    if signin_resp.status_code != 200:
        print(f"❌ Sign-in failed: {signin_resp.status_code}")
        print(f"📦 Response: {signin_resp.text}")
        exit(1)

    signin_data = signin_resp.json()
    if signin_data.get("code") != 200 or not signin_data.get("data"):
        print(f"❌ Sign-in failed: {signin_data}")
        exit(1)

    new_token = signin_data["data"].get("token") or signin_data["data"].get("accessToken")
    if not new_token:
        print("❌ No new token found in sign-in response.")
        print(f"📦 Full response: {signin_data}")
        exit(1)

    log("📡 Checking credits via /pricing...")
    pricing_headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json",
    }

    pricing_resp = requests.post(PRICING_URL, headers=pricing_headers)
    if pricing_resp.status_code != 200:
        print(f"❌ Failed to fetch pricing. Status: {pricing_resp.status_code}")
        print(f"📦 Response: {pricing_resp.text}")
        exit(1)

    try:
        pricing_data = pricing_resp.json()
    except Exception as e:
        print(f"❌ Failed to decode JSON: {e}")
        print(f"📦 Raw response (start): {pricing_resp.text[:300]}")
        exit(1)

    print("✅ Credit check-in successful!")
    print(f"👤 User: {pricing_data['data']['userName']}")
    print(f"💳 Credits: {pricing_data['data']['credits']}")

if __name__ == "__main__":
    main()
