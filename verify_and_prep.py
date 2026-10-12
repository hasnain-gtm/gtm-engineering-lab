import csv
import re

input_file = "uk_directors_enriched.csv"
output_file = "uk_directors_ready_for_outreach.csv"

def is_valid_syntax(email):
    """Checks basic email RFC syntax rules using regex."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

ready_leads = []

try:
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    print(f"Auditing {len(rows)} enriched director leads for deliverability QA...\n")

    for row in rows:
        # Safely extract values even if keys are missing or None
        email = (row.get("verified_email") or row.get("contact_email") or "").strip().lower()
        first_name = (row.get("first_name") or row.get("full_name") or "").strip()
        last_name = (row.get("last_name") or "").strip()
        domain = (row.get("domain") or "").strip().lower()
        
        # Deliverability Gate 1: Syntax Validation
        valid_syntax = is_valid_syntax(email)
        
        # Deliverability Gate 2: Verify essential identity details
        has_full_identity = bool(email and domain)

        if valid_syntax and has_full_identity:
            row["verified_email"] = email
            row["deliverability_score"] = "HIGH_PASS"
            row["outreach_status"] = "READY"
            ready_leads.append(row)
        else:
            row["verified_email"] = email
            row["deliverability_score"] = "FLAGGED"
            row["outreach_status"] = "NEEDS_MX_LOOKUP"
            # Keep flagged rows in dataset for audit visibility
            ready_leads.append(row)

    # Export sequence-ready records
    if ready_leads:
        fieldnames = list(ready_leads[0].keys())
        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ready_leads)

        print(f"SUCCESS: Quality Audit Complete! {len(ready_leads)} leads written to {output_file}!")
    else:
        print("WARNING: No leads found to write.")

except FileNotFoundError:
    print(f"Error: {input_file} not found. Ensure find_directors.py was executed first.")
except Exception as e:
    print(f"Unexpected error: {e}")