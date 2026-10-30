# PatientPilot AI — Healthcare Navigation Web App

**[▶ Try the public demo](https://patientpilot-ai-dwit.streamlit.app/)** · **[Architecture](ARCHITECTURE.md)** · **[Deployment guide](DEPLOYMENT.md)** · **[CI tests](https://github.com/damndwit/patientpilot-ai-health-navigator/actions)**

> **Portfolio prototype — synthetic data only.** Not a clinical product or patient care service. No actual appointments, prescriptions, insurance transactions, or transportation bookings.

**Current prototype: patient portal, AI record assistant, consent-based workflows, FHIR sandbox explorer and care navigation**

PatientPilot is a portfolio project exploring a single place to navigate patient information, care coordination, and eventually AI-assisted healthcare tasks. The current implementation includes a **read-only Streamlit dashboard with fictional FHIR-style health records** and a patient-specific chatbot. The chatbot works offline with retrieved facts; optional Gemini AI can explain those facts using a configured API key. An approval-controlled Care Actions interface simulates administrative requests. **No real healthcare systems are connected and no messages or requests are sent.**

## Portfolio highlight

Built a modular Python/Streamlit prototype combining record-grounded AI question answering, synthetic FHIR-style patient charts, read-only public FHIR sandbox exploration and patient-consent-gated **simulated** administrative workflows. The app is designed to be reviewed in a browser and discussed with source code and automated tests.

**Public demo:** [patientpilot-ai-dwit.streamlit.app](https://patientpilot-ai-dwit.streamlit.app/) — deployed by the project owner. The hosted app's full acceptance-test checklist is still pending independent confirmation.

## Current functionality

- Choose between two **fictional** patient profiles, each with separate records.
- View conditions, allergies, medications, clinical visits, laboratory results and reports.
- View sample appointments, fictional insurance coverage, and emergency contacts.
- Search available records using local keyword matching, and ask questions using a homepage chatbot with cited synthetic record IDs.
- Optional Gemini 2.5 Flash-Lite explanations using retrieved patient-scoped records and a private API key.
- Explore structured JSON data modeled on FHIR resources.
- Prepare fictional appointment inquiries, refill inquiries, clinic messages and insurance questions; explicitly approve or reject a draft.
- Review and download an **in-memory, patient-scoped demo audit log**; simulated approval never books an appointment or sends a request.
- Explore a public read-only SMART Health IT FHIR R4 synthetic sandbox in a separate tab (network availability permitting).
- Prepare public Google Maps hospital searches and driving directions without sending patient records or booking a ride.
- Run automated patient-isolation, consent and integration-client tests via GitHub Actions.

### Safety and privacy

**Synthetic data only.** There are no real patients, insurance accounts, doctors, clinics, pharmacy connections, live appointment bookings, ride bookings, or prescription requests. This is not a medical device or a production healthcare platform and must not be used for diagnosis, treatment or emergency response. Do not upload private patient records or enter identifying health information into a public demo.

The repository contains FHIR-*style* resources for learning. It has not been validated as fully conformant FHIR or connected to a FHIR server.

## Quick demonstration

1. Choose Alex Morgan or Jamie Brooks (fictional).
2. Ask **“What was my last cholesterol result?”** and inspect the cited local record IDs.
3. Explore labs, medications, appointments and coverage without leaving the app.
4. Open **Care Actions**, draft an appointment request, explicitly approve it, and view the in-session audit event. **Nothing is sent.**
5. Try **FHIR Sandbox** to inspect a separate synthetic public test server.
6. Try **Care Navigation** to open hospital search or driving directions in Maps.

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

## Screenshots

The following three screenshots were uploaded from the application on October 30, 2026. The filename numbers are used only to distinguish the images.

**Application screenshot 1**

![PatientPilot app screenshot 1](Screenshot%202026-10-30%20002839.png)

**Application screenshot 2**

![PatientPilot app screenshot 2](Screenshot%202026-10-30%20003010.png)

**Application screenshot 3**

![PatientPilot app screenshot 3](Screenshot%202026-10-30%20003047.png)

> Screenshots illustrate the demo application, not actual clinical workflows. All depicted patient records should be fictional. If a screenshot contains secrets or identifying personal information, remove it immediately and rotate any exposed API keys.

## Project files

- `app.py` — Streamlit patient dashboard, homepage chat, and navigation
- `care_ui.py` — administrative request preparation, review, consent, and demo audit log
- `workflows.py` — deterministic action validation, optional LLM intent suggestion and patient isolation
- `tests/test_workflows.py` — consent, isolation and no-side-effect tests
- `fhir_sandbox.py` — read-only bounded SMART Health IT public FHIR R4 client
- `navigation.py` — public map search and route URL helpers
- `navigation_ui.py` — FHIR explorer and navigation interface
- `tests/test_integrations.py` — mock FHIR and navigation URL tests
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

## FHIR sandbox and care navigation

The **🔗 FHIR Sandbox** tab queries only the public synthetic endpoint at `https://r4.smarthealthit.org` using allowlisted read-only GET requests with capped response sizes. It reads the test server's FHIR CapabilityStatement and lets you inspect up to five test patients and up to five associated observations. This data **does not become part of the local patient chart**, and the sandbox patient records are not real healthcare data. If the sandbox is unavailable, the rest of the app keeps working.

The **🧭 Care Navigation** tab offers a user-entered city/ZIP hospital search and user-entered origin/destination driving-directions link using Google Maps URLs. It displays demo appointments and fictional emergency contacts. It **cannot** identify an in-network hospital, guarantee operating hours, reserve a taxi, notify a clinic, or send data to healthcare systems. Google Maps opens externally; users should avoid entering sensitive patient information.

## Planned milestones

- [x] **1. Patient dashboard:** synthetic patients, labs, medications, encounters, coverage, appointments, contacts and keyword search
- [x] **2. Record-grounded assistant:** patient-specific sourced lookup works without an API key. Optional Gemini integration is implemented but requires key configuration and live testing.
- [x] **3. FHIR sandbox demo:** implement read-only synthetic test-server exploration. Public connectivity remains dependent on sandbox availability.
- [x] **4. Approval-controlled simulated actions:** request classification, drafts, explicit approve/reject decisions and in-session audit records. Nothing is actually submitted.
- [x] **5. Care navigation MVP:** hospital search and driving-directions links, fictional appointments and emergency contacts; no ride booking.
- [x] **6. Deployment & portfolio evidence:** public app URL, three screenshots, architecture and deployment documentation, plus passing GitHub Actions tests. Final hosted-app smoke testing remains recommended.

## Resume-ready project summary

**PatientPilot AI — Healthcare Navigation Web App** | Python, Streamlit, Gemini API, JSON/FHIR-style resources, GitHub Actions

- Developed a multi-patient healthcare demonstration dashboard backed by fictional FHIR-style records, including lab reports, medications, appointments, insurance data and record-scoped search.
- Integrated optional Gemini-based record-grounded question answering with cited evidence, offline fallback and explicit separation of synthetic data from public FHIR sandbox results.
- Implemented consent-gated administrative request simulations for appointments, refills and insurer messages, with patient-scoped checks, no outbound side effects and an in-session audit trail.
- Added a read-only SMART Health IT FHIR R4 sandbox explorer, hospital search/directions links, automated Python tests and software architecture documentation.

Use only claims you can personally demonstrate; **do not claim** real healthcare system integrations, actual prescription refills, HIPAA compliance, clinical accuracy or genuine bookings.

## Stack and learning references

Python · Streamlit · JSON · FHIR-style resources · unittest · GitHub Actions

- [Synthea](https://github.com/synthetichealth/synthea) — synthetic healthcare data inspiration
- [HL7 FHIR](https://hl7.org/fhir/) — interoperability standard
- [Medplum](https://github.com/medplum/medplum) — FHIR application reference
- [LangGraph](https://github.com/langchain-ai/langgraph) — possible future agent workflow reference

All included records are original, fabricated demo examples, not exports from a real clinical system or copied real patient data.

Created by [Dwit Patel](https://github.com/damndwit).
