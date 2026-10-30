# PatientPilot AI — architecture and engineering notes

## System boundaries

```text
Visitor's browser (Streamlit UI)
   |  selects a fictional patient; asks a question; drafts an action
   v
app.py (navigation, chat, demo-only notices)
   +-- records.py -> local synthetic FHIR-style JSON bundle (read only)
   +-- assistant.py -> patient-scoped evidence retrieval
   |      +-- offline record answer
   |      +-- optional Gemini 2.5 Flash-Lite API, opt-in, synthetic excerpts only
   +-- care_ui.py -> workflows.py
   |      +-- allowlisted action categories -> draft -> explicit consent
   |      +-- in-memory session decision log; NO outbound healthcare requests
   +-- navigation_ui.py -> fhir_sandbox.py
   |      +-- read-only GET to public synthetic SMART Health IT FHIR R4 test server
   +-- navigation.py
          +-- Google Maps public search/directions links (no ride booking)
```

## Design choices

**Patient data scoping:** Each chat query and simulated care-action validates the selected synthetic patient before referencing resources. The remote sandbox uses separate test patients and cannot modify local records.

**Grounded answering:** The chatbot retrieves relevant local record excerpts and shows source resource IDs. Without a Gemini key, deterministic record lookup works. With a key, Gemini generates a paraphrase based on the retrieved excerpts. This retrieval is heuristic; supporting references should be reviewed and are not proof that every model assertion is correct.

**Human approval:** The system permits only administrative request categories; patient consent changes a *demo state*, never a real clinic/insurer system. Tests verify cross-patient medication and approval checks.

**Privacy boundaries:** No account authentication, encryption-at-rest for client records, signed EHR integrations, durable audit records, or HIPAA compliance is claimed. Do not use this demo for real data.

**Availability and cost:** Public FHIR test servers and free inference quotas can be unavailable or rate-limited. Gemini is disabled until explicitly toggled on, but session-level limits do not control account-wide API usage.

## Testing

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q app.py assistant.py records.py workflows.py care_ui.py fhir_sandbox.py navigation.py navigation_ui.py tests
```

GitHub Actions runs automated unit tests. Interactions on the hosted application, external sandbox availability and actual model behavior require separate manual validation.

## Next engineering upgrades

- Persistent encrypted per-user data store with actual authentication/authorization.
- Approved SMART-on-FHIR OAuth workflow and individual provider integration, with sandbox testing first.
- Durable patient audit history and robust secure action execution.
- Clinical review of any health-advice feature before patient-facing use.
- Rate limiting and spending controls across all deployed users.
