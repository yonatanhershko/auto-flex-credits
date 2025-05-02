import requests
import os
import json

BASE_URL = "https://api2.tap4.ai"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
}

SITE = "flux-ai.io"
EMAIL = os.environ.get("FLUX_EMAIL")  # optional
TOKEN = os.environ.get("FLUX_BEARER_TOKEN")

def log(msg):
    print(f"🔹 {msg}")

def sign_in():
    log("Signing in...")
    res = requests.post(
        f"{BASE_URL}/signIn",
        headers=HEADERS,
        json={"site": SITE}
    )
    try:
        res.raise_for_status()
        data = res.json()
        if data.get("code") != 200:
            raise Exception(f"Unexpected response code: {data}")
        log("✅ Sign-in success.")
    except Exception as e:
        print(f"❌ Sign-in failed: {e}")
        print(f"📦 Response: {res.text}")
        exit(1)

def check_credits():
    log("Checking credits...")
    headers = {**HEADERS, "Authorization": f"Bearer {TOKEN}"}
    res = requests.post(
        f"{BASE_URL}/pricing",
        headers=headers,
        json={"site": SITE}
    )
    try:
        res.raise_for_status()
        if "application/json" not in res.headers.get("Content-Type", ""):
            raise ValueError("Response is not JSON")

        data = res.json()
        credits = data["data"]["credits"]
        log(f"💰 Current credits: {credits}")
    except Exception as e:
        print(f"❌ Failed to check credits: {e}")
        print(f"📦 Response text: {res.text}")
        exit(1)

if __name__ == "__main__":
    log("📡 Starting Flux AI daily credit check-in...")
    sign_in()
    check_credits()
