import os
import requests
import smtplib
from email.mime.text import MIMEText
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

def send_email_alert(subject, message):
    """Send email notification with check-in results"""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = os.getenv("FLUX_EMAIL")
    
    try:
        print("📨 Sending email notification...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        print("✅ Email sent")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

# Main execution
print("🔹 📡 Starting Flux AI daily credit check-in...")
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
email_subject = f"Flux AI Check-in Result - {current_date}"
email_body = f"Flux AI Check-in Results - {current_date}\n\n"

try:
    response = requests.post(SIGNIN_URL, json=PAYLOAD, headers=HEADERS)
    print(f"🔹 HTTP {response.status_code}")
    email_body += f"HTTP Status: {response.status_code}\n"
    
    # Attempt to parse JSON
    try:
        data = response.json()
    except ValueError:
        error_msg = "❌ Failed to decode JSON.\n"
        error_msg += f"📦 Raw response (start): {response.text[:500]}"
        print(error_msg)
        email_body += error_msg
        send_email_alert(email_subject, email_body)
        exit(1)
    
    if data.get("code") == 200:
        success_msg = "✅ Check-in successful!"
        print(success_msg)
        email_body += success_msg
        
        # Add user data to email if available
        user_name = None
        credits = None
        
        if "data" in data:
            if "userName" in data["data"]:
                user_name = data["data"]["userName"]
                email_body += f"\n👤 User: {user_name}"
            
            if "credits" in data["data"]:
                credits = data["data"]["credits"]
                email_body += f"\n💳 Credits: {credits}"
                
    elif data.get("msg", "").lower().startswith("checked in today"):
        already_msg = "✅ Already checked in today."
        print(already_msg)
        email_body += already_msg
    else:
        unexpected_msg = f"⚠️ Unexpected response: {data}"
        print(unexpected_msg)
        email_body += unexpected_msg
        send_email_alert(email_subject, email_body)
        exit(1)
except Exception as e:
    exception_msg = f"❌ Exception occurred: {e}"
    print(exception_msg)
    email_body += exception_msg
    send_email_alert(email_subject, email_body)
    exit(1)

# Send success email
send_email_alert(email_subject, email_body)
