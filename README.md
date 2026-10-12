# 🚀 Automated Multi-Channel GTM Outbound Pipeline

An end-to-end, code-driven Go-To-Market (GTM) engineering pipeline built in Python. This system automates B2B target account extraction, legal company name regex normalization, decision-maker enrichment, RFC deliverability auditing, and multi-channel campaign dispatch (Email + LinkedIn) at $0 infrastructure cost.

---

## 🏗️ Pipeline Architecture

```text
 1. Account Sourcing     2. Name Normalization    3. Persona Sourcing
┌────────────────────┐   ┌────────────────────┐   ┌──────────────────────┐
│ Apollo API         │──►│ Custom Python      │──►│ Decision-Maker       │
│ (X-Api-Key Header) │   │ Regex Normalizer   │   │ Profile Sourcing     │
└────────────────────┘   └────────────────────┘   └──────────────────────┘
                                                             │
                                                             ▼
 5. Campaign Dispatch    4. Deliverability QA     ┌──────────────────────┐
┌────────────────────┐   ┌────────────────────┐   │ Clean Output         │
│ Local Mock Server  │◄──│ Syntax Validation  │◄──│ uk_directors_        │
│ (Email + LinkedIn) │   │ & Identity Scoring │   │ enriched.csv         │
└────────────────────┘   └────────────────────┘   └──────────────────────┘

💡 Key Features & Modules

Account Extraction (fetch_real_apollo_leads.py): Sources live target company records via header-based REST API calls (X-Api-Key).

Data Normalization (clean_companies.py): Uses custom regex patterns to strip legal suffixes (Ltd, LLC, Group) for natural outreach merge tags ({{clean_company_name}}).

Persona Enrichment (find_directors.py): Extracts decision-maker profiles (Managing Directors, Sales Directors, Finance Directors) mapped to target domains.

Deliverability QA Engine (verify_and_prep.py): Audits RFC email syntax and identity completeness, tagging verified leads with HIGH_PASS status to keep campaign bounce rates below 2%.

Multi-Channel Dispatch (upload_to_sequencer.py & mock_instantly_server.py): Formats and transmits lead batches over HTTP POST to local mock REST endpoints representing email sequencers (Smartlead/Instantly) and LinkedIn automation platforms (HeyReach).

Master Orchestrator (main_pipeline.py): Executes the entire 5-stage workflow sequentially with a single CLI command.

🛠️ Tech Stack & Prerequisites
Language: Python 3.13 (Standard Libraries: urllib.request, json, re, csv, http.server, subprocess)

Environment: VS Code, PowerShell, Git/GitHub

Integrations: Apollo API, Smartlead API schema, HeyReach API schema