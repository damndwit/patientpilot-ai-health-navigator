# PatientPilot AI — Healthcare Navigation Web App

**Milestone 2: Patient portal + record-grounded chatbot (prototype)**

PatientPilot is a portfolio project exploring a single place to navigate patient information, care coordination, and eventually AI-assisted healthcare tasks. The current implementation includes a **read-only Streamlit dashboard with fictional FHIR-style health records** and a patient-specific chatbot. The chatbot works offline with retrieved facts; optional Gemini AI can explain those facts using a configured API key. No real healthcare systems are connected.

## Current functionality

- Choose between two **fictional** patient profiles, each with separate records.
- View conditions, allergies, medications, clinical visits, laboratory results and reports.
- View sample appointments, fictional insurance coverage, and emergency contacts.
- Search available records using local keyword matching, and ask questions using a homepage chatbot with cited synthetic record IDs.
- Optional Gemini 2.5 Flash-Lite explanations using retrieved patient-scoped records and a private API key.
- Explore structured JSON data modeled on FHIR resources.
- Run automated data-access tests via GitHub Actions.

### Safety and privacy

**Synthetic data only.** There are no real patients, insurance accounts, doctors, clinics, pharmacy connections, live appointment bookings, ride bookings, or prescription requests. This is not a medical device or a production healthcare platform and must not be used for diagnosis, treatment or emergency response. Do not upload private patient records or enter identifying health information into a public demo.

The repository contains FHIR-*style* resources for learning. It has not been validated as fully conformant FHIR or connected to a FHIR server.

## Getting started

You can run the app in GitHub Codespaces, or on a local computer with Python 3.10+:

```bash
git clone https://github.com/damndwit/patientpilot-ai-health-navigator.git
cd patientpilot-ai-health-navigator
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the forwarded port 8501 (or `http://localhost:8501`) to see the dashboard.

Run tests with:

```bash
python -m unittest discover -s tests -v
```

## Optional free-tier Gemini setup

The chatbot works *without any API key* in local record-lookup mode. To use a hosted LLM, create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey). In your running Codespace, create a local file `.streamlit/secrets.toml` with:

```toml
GEMINI_API_KEY = "YOUR_KEY_HERE"
```

**Do not commit this file to GitHub.** It's ignored by `.gitignore`. To deploy with Streamlit Community Cloud, open your app's **Manage app → Settings → Secrets** and enter the same TOML text there. Never share the key in chat or screenshots. Use only fictional patient records; Google API free-tier data handling is not designed here for real patient medical information.

Install requirements and restart Streamlit after pulling the latest code:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Project files

- `app.py` — Streamlit patient dashboard, homepage chat, and navigation
- `assistant.py` — source-grounded chatbot and optional Gemini integration
- `tests/test_assistant.py` — patient isolation, fallback, and retrieval tests
- `records.py` — synthetic resource parsing, patient scoping and keyword search
- `data/synthetic_fhir_bundle.json` — 25 fictional FHIR-style records
- `tests/test_records.py` — data integrity and patient isolation checks
- `.github/workflows/tests.yml` — automated syntax and unit tests
- `.streamlit/config.toml` — demo interface theme

## Planned milestones

- [x] **1. Patient dashboard:** synthetic patients, labs, medications, encounters, coverage, appointments, contacts and keyword search
- [x] **2. Record-grounded assistant:** patient-specific sourced lookup works without an API key. Optional Gemini integration is implemented but requires key configuration and live testing.
- [ ] **3. FHIR sandbox:** demonstrate authorized integration using publicly available test data
- [ ] **4. Approval-controlled simulated actions:** draft appointment and refill inquiries, approve/reject workflow, audit events
- [ ] **5. Care navigation:** demonstration of hospital lookup, contacts, and ride-planning concepts
- [ ] **6. Deployment & portfolio proof:** deploy public demo, screenshots, architecture, and passing tests

## Stack and learning references

Python · Streamlit · JSON · FHIR-style resources · unittest · GitHub Actions

- [Synthea](https://github.com/synthetichealth/synthea) — synthetic healthcare data inspiration
- [HL7 FHIR](https://hl7.org/fhir/) — interoperability standard
- [Medplum](https://github.com/medplum/medplum) — FHIR application reference
- [LangGraph](https://github.com/langchain-ai/langgraph) — possible future agent workflow reference

All included records are original, fabricated demo examples, not exports from a real clinical system or copied real patient data.

Created by [Dwit Patel](https://github.com/damndwit).
