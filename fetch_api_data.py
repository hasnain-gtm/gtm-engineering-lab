import json
import urllib.request
import csv

# Step 1: Query the REST API endpoint
url = "https://jsonplaceholder.typicode.com/users/1"
req = urllib.request.urlopen(url)
raw_data = req.read().decode("utf-8")

# Step 2: Parse raw string into structured Python JSON (Dictionary)
user_data = json.loads(raw_data)

# Step 3: Extract specific target fields for GTM enrichment
lead_record = {
    "full_name": user_data["name"],
    "email": user_data["email"],
    "company_name": user_data["company"]["name"],
    "website": user_data["website"]
}

# Step 4: Export directly to a clean CSV
with open("api_leads.csv", "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=lead_record.keys())
    writer.writeheader()
    writer.writerow(lead_record)

print("SUCCESS: Lead successfully fetched from API and saved to api_leads.csv!")