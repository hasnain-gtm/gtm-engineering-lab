import json
import urllib.request
import csv

# Your active free Apollo API Key
APOLLO_API_KEY = "9DLU7rZh6Y53GIzl_V0tTw"

# Apollo Free Tier allows Organization Search
url = "https://api.apollo.io/v1/organizations/search"

# Define UK SMB Target Company Parameters
payload = {
    "organization_locations": ["United Kingdom"],
    "organization_num_employees_ranges": ["11,50", "51,200"],
    "page": 1,
    "per_page": 25
}

data = json.dumps(payload).encode("utf-8")

# Authentication MUST go in the HTTP Header as 'X-Api-Key'
headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "X-Api-Key": APOLLO_API_KEY
}

req = urllib.request.Request(url, data=data, headers=headers)

try:
    print("Fetching Target UK SMB Companies from Apollo API...")
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode("utf-8"))
    organizations = result.get("organizations", [])

    if not organizations:
        print("No organizations returned. Verify query filters.")
    else:
        companies = []
        for org in organizations:
            companies.append({
                "company_id": org.get("id"),
                "company_name": org.get("name"),
                "primary_domain": org.get("primary_domain"),
                "employees": org.get("estimated_num_employees"),
                "city": org.get("city"),
                "country": org.get("country")
            })

        # Save to CSV
        with open("uk_target_companies.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=companies[0].keys())
            writer.writeheader()
            writer.writerows(companies)

        print(f"\nSUCCESS: Extracted {len(companies)} UK SMB Target Companies into uk_target_companies.csv!")

except urllib.error.HTTPError as e:
    print(f"\nHTTP Error {e.code}: {e.reason}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"\nUnexpected Error: {e}")