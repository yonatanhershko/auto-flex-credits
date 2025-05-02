import requests
import os

def get_flux_credit():
    token = os.getenv("FLUX_BEARER_TOKEN")

    if not token:
        print("❌ No token provided in FLUX_BEARER_TOKEN")
        exit(1)

    url = "https://flux-ai.io/pricing/"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (GitHubActionBot/1.0)"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            credits = data.get("data", {}).get("credits")
            print(f"✅ Flux Credits: {credits}")
        else:
            print("⚠️ Unexpected response:", data)
            exit(1)

    except Exception as e:
        print("❌ Error:", e)
        exit(1)

if __name__ == "__main__":
    get_flux_credit()
