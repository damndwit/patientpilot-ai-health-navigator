# PatientPilot AI — Healthcare Navigation Web App

**Milestone 1: Synthetic patient portal (prototype)**

PatientPilot is a portfolio project exploring a single place to navigate patient information, care coordination, and eventually AI-assisted healthcare tasks. The current implementation is a **read-only Streamlit dashboard with fictional FHIR-style health records**. An LLM and external healthcare connections are **not yet implemented**.

## Current functionality

- Choose between two **fictional** patient profiles, each with separate records.
- View conditions, allergies, medications, clinical visits, laboratory results and reports.
- View sample appointments, fictional insurance coverage, and emergency contacts.
- Search available records using local keyword matching.
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

## Project files

- `app.py` — Streamlit patient dashboard and navigation
- `records.py` — synthetic resource parsing, patient scoping and keyword search
- `data/synthetic_fhir_bundle.json` — 25 fictional FHIR-style records
- `tests/test_records.py` — data integrity and patient isolation checks
- `.github/workflows/tests.yml` — automated syntax and unit tests
- `.streamlit/config.toml` — demo interface theme

## Planned milestones

- [x] **1. Patient dashboard:** synthetic patients, labs, medications, encounters, coverage, appointments, contacts and keyword search
- [ ] **2. LLM + record-grounded retrieval:** free-tier model using synthetic data; responses cite records and refuse unsupported claims
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
