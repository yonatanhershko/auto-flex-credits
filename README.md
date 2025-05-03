GitHub Workflow (YAML)
      │
      ▼
מריץ את הקובץ flux_daily_checkin.py
      │
      ▼
1. קורא את הטוקן מהסביבה (FLUX_TOKEN)
      │
      ▼
2. שולח בקשת POST ל־https://api2.tap4.ai/signIn
      │
      ▼
3. אם ההתחברות הצליחה → שולח בקשת GET ל־https://flux-ai.io/pricing/
      │
      ▼
4. מנסה להדפיס את הקרדיטים או את השגיאה שקיבל
 
