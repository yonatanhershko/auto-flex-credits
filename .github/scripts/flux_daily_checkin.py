import os
import requests
import json
from datetime import datetime

# Flux API endpoints
SIGNIN_URL = 'https://api2.tap4.ai/signIn'

# Headers for API requests
HEADERS = {
    'Authorization': f"Bearer {os.getenv('FLUX_TOKEN')}",
    'Content-Type': 'application/json',
    'Accept': '*/*'
}

# Payload for API requests
PAYLOAD = {'site': 'flux-ai.io'}

# For GitHub Actions output
def set_github_output(name, value):
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"{name}={value}\n")

def set_github_summary(message):
    with open(os.environ.get('GITHUB_STEP_SUMMARY', '/dev/null'), 'a') as f:
        f.write(f"{message}\n")

# Main execution
print("🔹 📡 Starting Flux AI daily credit check-in...")
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
summary = f"# Flux AI Check-in Results - {current_date}\n\n"

try:
    response = requests.post(SIGNIN_URL, json=PAYLOAD, headers=HEADERS)
    print(f"🔹 HTTP {response.status_code}")
    summary += f"**HTTP Status:** {response.status_code}\n\n"
    
    # Attempt to parse JSON
    try:
        data = response.json()
    except ValueError:
        error_msg = "❌ Failed to decode JSON.\n"
        error_msg += f"```\n{response.text[:500]}\n```"
        print(error_msg)
        summary += error_msg
        set_github_output("status", "error")
        set_github_output("message", "Failed to decode JSON response")
        set_github_summary(summary)
        exit(1)
    
    if data.get("code") == 200:
        success_msg = "✅ Check-in successful!"
        print(success_msg)
        summary += f"### {success_msg}\n\n"
        
        # Add user data to summary if available
        user_name = None
        credits = None
        
        if "data" in data:
            if "userName" in data["data"]:
                user_name = data["data"]["userName"]
                summary += f"**User:** {user_name}\n\n"
                set_github_output("username", user_name)
            
            if "credits" in data["data"]:
                credits = data["data"]["credits"]
                summary += f"**Credits:** {credits}\n\n"
                set_github_output("credits", str(credits))
                
        set_github_output("status", "success")
        set_github_output("message", "Check-in successful")
        
    elif data.get("msg", "").lower().startswith("checked in today"):
        already_msg = "✅ Already checked in today."
        print(already_msg)
        summary += f"### {already_msg}\n\n"
        set_github_output("status", "already_checked_in")
        set_github_output("message", "Already checked in today")
    else:
        unexpected_msg = f"⚠️ Unexpected response: {json.dumps(data, indent=2)}"
        print(unexpected_msg)
        summary += f"### ⚠️ Unexpected Response\n\n```json\n{json.dumps(data, indent=2)}\n```\n\n"
        set_github_output("status", "unexpected")
        set_github_output("message", "Unexpected API response")
        set_github_summary(summary)
        exit(1)
except Exception as e:
    exception_msg = f"❌ Exception occurred: {e}"
    print(exception_msg)
    summary += f"### ❌ Error\n\n{exception_msg}\n\n"
    set_github_output("status", "error")
    set_github_output("message", str(e))
    set_github_summary(summary)
    exit(1)

# Add final summary to GitHub Actions
set_github_summary(summary)
