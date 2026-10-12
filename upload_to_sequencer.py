import csv
import json
import urllib.request

CSV_FILE = "uk_directors_ready_for_outreach.csv"

# Endpoint Configurations
EMAIL_API_URL = "http://127.0.0.1:5000/v1/email/campaign"
LINKEDIN_API_URL = "http://127.0.0.1:5000/v1/linkedin/campaign"

API_KEY = "FAKE_MULTI_CHANNEL_KEY_999"

def load_ready_leads(file_path):
    email_leads = []
    linkedin_leads = []
    
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("deliverability_score") == "HIGH_PASS":
                # Email Payload
                email_leads.append({
                    "email": row.get("verified_email"),
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "company_name": row.get("company_name")
                })
                # LinkedIn Payload (Constructing targeted profile URL)
                first = (row.get("first_name") or "").lower()
                last = (row.get("last_name") or "").lower()
                linkedin_leads.append({
                    "linkedin_url": f"https://www.linkedin.com/in/{first}-{last}-uk",
                    "first_name": row.get("first_name"),
                    "company_name": row.get("company_name"),
                    "connection_note": f"Hi {row.get('first_name')}, saw your work at {row.get('company_name')}. Would love to connect!"
                })
                
    return email_leads, linkedin_leads

try:
    email_batch, linkedin_batch = load_ready_leads(CSV_FILE)
    print(f"\n[MULTI-CHANNEL] Loaded {len(email_batch)} Email leads and {len(linkedin_batch)} LinkedIn profiles...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 1. Dispatch Email Sequence
    email_req = urllib.request.Request(
        EMAIL_API_URL, 
        data=json.dumps({"campaign_id": "email_uk_directors_v1", "leads": email_batch}).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    email_resp = json.loads(urllib.request.urlopen(email_req).read().decode("utf-8"))
    print(f"\n[EMAIL QUEUE]: {email_resp.get('message')}")

    # 2. Dispatch LinkedIn Sequence (HeyReach Pattern)
    linkedin_req = urllib.request.Request(
        LINKEDIN_API_URL, 
        data=json.dumps({"campaign_id": "linkedin_uk_directors_v1", "leads": linkedin_batch}).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    linkedin_resp = json.loads(urllib.request.urlopen(linkedin_req).read().decode("utf-8"))
    print(f"[LINKEDIN QUEUE]: {linkedin_resp.get('message')}")

except Exception as e:
    print(f"Multi-Channel Upload Error: {e}")