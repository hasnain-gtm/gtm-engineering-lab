import csv
import json
import urllib.request

CSV_FILE = "uk_directors_ready_for_outreach.csv"

# Mock parameters for practice execution
SEQUENCER_API_KEY = "FAKE_INSTANTLY_API_KEY_123"
CAMPAIGN_ID = "camp_uk_smb_directors_v1"
API_URL = "http://127.0.0.1:5000/v1/lead/add"

def load_ready_leads(file_path):
    """Filters dataset for HIGH_PASS audited leads and formats merge tags."""
    leads = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("deliverability_score") == "HIGH_PASS":
                leads.append({
                    "email": row.get("verified_email"),
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "company_name": row.get("company_name"),
                    "custom_variables": {
                        "clean_company_name": row.get("company_name"),
                        "title": row.get("exact_title") or row.get("target_title"),
                        "domain": row.get("domain")
                    }
                })
    return leads

try:
    leads_to_upload = load_ready_leads(CSV_FILE)
    print(f"\n[CLIENT] Filtered {len(leads_to_upload)} HIGH_PASS leads for API transmission...")

    # Package request payload
    payload_data = {
        "campaign_id": CAMPAIGN_ID,
        "leads": leads_to_upload
    }
    
    payload = json.dumps(payload_data).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SEQUENCER_API_KEY}"
    }

    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
    
    print("[CLIENT] Transmitting payload to local practice endpoint...")
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode("utf-8"))

    print("\n[CLIENT HTTP 200 SUCCESS RESPONSE]")
    print(json.dumps(result, indent=2))

except FileNotFoundError:
    print(f"Error: {CSV_FILE} not found. Ensure verify_and_prep.py ran successfully.")
except Exception as e:
    print(f"Pipeline Upload Error: {e}")
    