import requests
import os

def get_flux_credit():
    print("📡 Starting credit check...")

    token = os.getenv("FLUX_BEARER_TOKEN")
    if not token:
        print("❌ Missing token in environment variable FLUX_BEARER_TOKEN")
        exit(1)

    url = "https://flux-ai.io/pricing/"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (GitHubActionBot/1.0)"
    }

    try:
        print(f"➡️ Sending POST request to {url}")
        response = requests.post(url, headers=headers)
        print(f"🔁 Status Code: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        print("📦 Response data received")

        if data.get("code") == 200 and "data" in data:
            credits = data["data"].get("credits", "N/A")
            user = data["data"].get("userName", "Unknown user")
            print(f"✅ User: {user} | Current Credits: {credits}")
        else:
            print(f"⚠️ Unexpected response: {data}")
            exit(1)

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        exit(1)

if __name__ == "__main__":
    get_flux_credit()
