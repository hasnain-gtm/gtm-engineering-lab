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