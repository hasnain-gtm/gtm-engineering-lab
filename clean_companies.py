import csv
import re

def clean_company_name(name):
    """
    Regex normalization: Strips legal suffixes (Ltd, Limited, LLC, Inc, Group, UK, Corp)
    and removes trailing punctuation or excess whitespace.
    """
    if not name:
        return ""
    
    # Define regex pattern for corporate legal suffixes
    pattern = r'\b(Inc\.?|LLC\.?|Corp\.?|Corporation|Ltd\.?|Limited|Group|Co\.?|UK|Pty)\b'
    
    # Strip matches ignoring case
    cleaned = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Clean up excess spaces or punctuation left behind
    cleaned = re.sub(r'[\s,\.-]+$', '', cleaned).strip()
    return cleaned if cleaned else name

# Process raw UK target companies file
input_file = "uk_target_companies.csv"
output_file = "uk_target_companies_cleaned.csv"

try:
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

        cleaned_rows = []
        for row in rows:
            raw_name = row.get("company_name", "")
            row["clean_company_name"] = clean_company_name(raw_name)
            row["domain"] = (row.get("primary_domain") or "").lower().strip()
            cleaned_rows.append(row)

    # Write normalized leads out
    if cleaned_rows:
        fieldnames = list(cleaned_rows[0].keys())
        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_rows)

        print(f"SUCCESS: Normalized {len(cleaned_rows)} company records into {output_file}!")

except FileNotFoundError:
    print(f"Error: {input_file} not found. Ensure fetch_real_apollo_leads.py ran successfully.")
except Exception as e:
    print(f"Unexpected error during normalization: {e}")