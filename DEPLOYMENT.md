# Public deployment guide — Streamlit Community Cloud

**This is a public portfolio demonstration using synthetic patients only.** Do not put real clinical records, personally identifying patient information, genuine prescriptions or client secrets in the repository or public app.

## Deployment

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
2. Create app → deploy an existing app from GitHub.
3. Use these settings:
   - Repository: `dwitdev/patientpilot-ai-health-navigator`
   - Branch: `main`
   - Main file path: `app.py`
   - Python: **3.12** if the platform asks you to choose
   - Optional subdomain: `patientpilot-ai-dwit` if available
4. **First deploy with no secrets.** The assistant works in deterministic record-retrieval mode, and all other tabs remain usable.
5. Once the public app is working, optionally open app settings → **Secrets** and enter `GEMINI_API_KEY = "your-key"` (do not put the key in GitHub, a screenshot, or a chat).
6. The homepage Gemini toggle is deliberately **off by default**; an enabled session is capped at 10 attempted Gemini requests. This is a demonstration safeguard, **not a global spending limit**. API costs and provider terms should be monitored separately.
7. Confirm the actual Streamlit URL before adding it to the project README or GitHub profile.

## Live acceptance checks

- Dashboard loads with fictional Alex and Jamie; changing patients does not expose the prior patient's chat or action history.
- Local search answers a cholesterol or appointment question and displays actual synthetic record references.
- Optional Gemini toggle defaults off; after entering the key and enabling it, the response can indicate Gemini mode.
- Create a care action, inspect the proposed draft, check explicit consent and approve it. The result must clearly say **demo-only / not sent**.
- Refuse a refill for a medication that belongs to the other fictional patient.
- FHIR Sandbox displays public R4 capability metadata or a friendly unavailable error; remote sandbox records remain separate.
- Care Navigation opens a hospital-search or directions URL without reserving a ride.
- The app looks usable at phone width. No medical interpretation or actual healthcare transactions are performed.

## Operational notes

- Streamlit Community Cloud is for learning and demos, **not approved here for real patient information**.
- GitHub Actions tests are not equivalent to medical validation or a privacy/security audit.
- Local session audit events are transient, not a durable healthcare audit trail.
- The FHIR sandbox is an unauthenticated public test endpoint, not a connection to a hospital EHR.
- If deployment errors occur, read Streamlit's app logs and run `python -m unittest discover -s tests -v` locally.
- GitHub repository updates ordinarily trigger Streamlit redeployment, so verify the new version after each change.

[Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
