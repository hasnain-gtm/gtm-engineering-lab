import subprocess
import sys
import time

def run_step(step_name, script_name):
    print("\n" + "=" * 60)
    print(f" Executing Pipeline Step: {step_name}")
    print("=" * 60)
    
    start_time = time.time()
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ ERROR: Step '{step_name}' failed during execution of {script_name}.")
        sys.exit(1)
        
    elapsed = round(time.time() - start_time, 2)
    print(f"\n   Step '{step_name}' completed successfully in {elapsed}s.")

def main():
    print("\n🚀 STARTING GTM OUTBOUND AUTOMATION PIPELINE")
    
    # 1. Fetch Target Companies from Apollo API
    run_step("1. Apollo Target Account Extraction", "fetch_real_apollo_leads.py")
    
    # 2. Normalize Legal Suffixes
    run_step("2. Company Name Regex Normalization", "clean_companies.py")
    
    # 3. Source Persona Decision-Makers
    run_step("3. Decision-Maker Persona Enrichment", "find_directors.py")
    
    # 4. Deliverability Audit & Quality Gate
    run_step("4. Deliverability Audit & QA Scoring", "verify_and_prep.py")
    
    # 5. Push to Sequencer / Mock Endpoint
    run_step("5. Automated Sequencer Payload Upload", "upload_to_sequencer.py")
    
    print("\n" + "*" * 60)
    print(" 🎉 END-TO-END PIPELINE EXECUTION COMPLETE!")
    print("    Ready dataset: uk_directors_ready_for_outreach.csv")
    print("*" * 60 + "\n")

if __name__ == "__main__":
    main()