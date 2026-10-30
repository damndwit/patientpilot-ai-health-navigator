# PatientPilot AI — Healthcare Navigation Web App

**Milestone 4 prototype: Patient portal, record-grounded chatbot and simulated care actions**

PatientPilot is a portfolio project exploring a single place to navigate patient information, care coordination, and eventually AI-assisted healthcare tasks. The current implementation includes a **read-only Streamlit dashboard with fictional FHIR-style health records** and a patient-specific chatbot. The chatbot works offline with retrieved facts; optional Gemini AI can explain those facts using a configured API key. An approval-controlled Care Actions interface simulates administrative requests. **No real healthcare systems are connected and no messages or requests are sent.**

## Current functionality

- Choose between two **fictional** patient profiles, each with separate records.
- View conditions, allergies, medications, clinical visits, laboratory results and reports.
- View sample appointments, fictional insurance coverage, and emergency contacts.
- Search available records using local keyword matching, and ask questions using a homepage chatbot with cited synthetic record IDs.
- Optional Gemini 2.5 Flash-Lite explanations using retrieved patient-scoped records and a private API key.
- Explore structured JSON data modeled on FHIR resources.
- Prepare fictional appointment inquiries, refill inquiries, clinic messages and insurance questions; explicitly approve or reject a draft.
- Review and download an **in-memory, patient-scoped demo audit log**; simulated approval never books an appointment or sends a request.
- Run automated data-access and approval-gate tests via GitHub Actions.

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
- `care_ui.py` — administrative request preparation, review, consent, and demo audit log
- `workflows.py` — deterministic action validation, optional LLM intent suggestion and patient isolation
- `tests/test_workflows.py` — consent, isolation and no-side-effect tests
- `assistant.py` — source-grounded chatbot and optional Gemini integration
- `tests/test_assistant.py` — patient isolation, fallback, and retrieval tests
- `records.py` — synthetic resource parsing, patient scoping and keyword search
- `data/synthetic_fhir_bundle.json` — 25 fictional FHIR-style records
- `tests/test_records.py` — data integrity and patient isolation checks
- `.github/workflows/tests.yml` — automated syntax and unit tests
- `.streamlit/config.toml` — demo interface theme

## Try the simulated action workflow

1. Open the **🧾 Care Actions** tab and describe a routine appointment or refill inquiry.
2. Click **Suggest request type**; Gemini may suggest an allowlisted category when configured. Otherwise keyword rules operate without an API key.
3. Select the request type, enter a short note, and choose the relevant fictional medication if needed.
4. Click **Prepare draft for my review**. Inspect the recipient, linked synthetic resource, and explicit no-transmission warning.
5. **Approve demo request** only after checking the consent box, or reject it. Inspect the audit log and optionally download the JSON.
6. Switch demo patients and verify that the other patient's draft and log are not visible.

No action contacts a clinic, pharmacy, insurer, or emergency service. The approval exists **only in your current browser session**, not in a persistent health system.

## Planned milestones

- [x] **1. Patient dashboard:** synthetic patients, labs, medications, encounters, coverage, appointments, contacts and keyword search
- [x] **2. Record-grounded assistant:** patient-specific sourced lookup works without an API key. Optional Gemini integration is implemented but requires key configuration and live testing.
- [ ] **3. FHIR sandbox:** demonstrate authorized integration using publicly available test data
- [x] **4. Approval-controlled simulated actions:** request classification, drafts, explicit approve/reject decisions and in-session audit records. Nothing is actually submitted.
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
