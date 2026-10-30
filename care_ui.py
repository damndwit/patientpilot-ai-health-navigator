"""Streamlit presentation for consent-gated *simulated* administrative workflows."""
from __future__ import annotations
import json
from dataclasses import asdict
from datetime import date, timedelta

import streamlit as st
from records import label
from workflows import (
    ACTION_TYPES, audit_entry, create_draft, decide, draft_summary,
    medications_for, suggest_kind,
)

def render_care_actions(bundle, patient_id, api_key=""):
    st.subheader("🧾 Care Actions — approval required")
    st.warning("DEMO ONLY: Requests are NOT sent, appointments are NOT booked, and prescriptions are NOT refilled. All data is fictional.")
    if st.session_state.get("care_patient") != patient_id:
        st.session_state.care_patient = patient_id
        st.session_state.care_draft = None
        st.session_state.care_history = []
        st.session_state.care_suggestion = None

    st.markdown("#### 1. Describe what you need")
    with st.form("care_suggestion_form"):
        request_text = st.text_area(
            "Ask PatientPilot to prepare an administrative request",
            placeholder="Example: Please help me request a follow-up appointment next month.",
            max_chars=500,
        )
        suggest = st.form_submit_button("Suggest request type", type="primary")
    if suggest:
        kind, mode = suggest_kind(request_text, api_key=api_key)
        st.session_state.care_suggestion = kind
        if kind:
            st.success(f"Suggested: {ACTION_TYPES[kind]} ({mode}). Review the type and details below.")
        else:
            st.info("No supported administrative request was identified. You can select a type manually.")
        st.session_state.care_draft = None

    st.markdown("#### 2. Create and review a draft")
    kinds = list(ACTION_TYPES)
    suggested_kind = st.session_state.get("care_suggestion")
    selected_index = kinds.index(suggested_kind) if suggested_kind in kinds else 0
    with st.form("care_draft_form"):
        kind = st.selectbox("Request type", kinds, index=selected_index, format_func=lambda x:ACTION_TYPES[x])
        note = st.text_area("Message or request details (demo only)", max_chars=500,
                            placeholder="Write the specific administrative request here.")
        preferred = st.date_input("Preferred visit date (only for appointment inquiries)",
                                  value=date.today()+timedelta(days=14))
        meds = medications_for(bundle, patient_id)
        med_options = [f"MedicationRequest/{item['id']}" for item in meds]
        med_labels = {f"MedicationRequest/{item['id']}":label(item) for item in meds}
        medication_ref = st.selectbox("Medication on demo record (only for refill inquiries)",
                                      ["", *med_options],
                                      format_func=lambda x:med_labels.get(x,"No medication selected"))
        submit = st.form_submit_button("Prepare draft for my review")
    if submit:
        try:
            draft = create_draft(bundle, patient_id, kind, note,
                     preferred_date=preferred.isoformat() if kind=="appointment_request" else "",
                     medication_ref=medication_ref if kind=="refill_inquiry" else "")
            st.session_state.care_draft = draft
            st.session_state.care_history.append(audit_entry(draft,"draft_created"))
            st.success("Draft prepared. Nothing has been sent.")
        except ValueError as exc:
            st.error(str(exc))
    draft = st.session_state.get("care_draft")
    if draft and draft.patient_id == patient_id:
        st.markdown("#### 3. Explicit patient decision")
        st.json(draft_summary(draft), expanded=True)
        if draft.status == "pending_review":
            consent = st.checkbox(
                "I have reviewed this fictional request. I authorize recording DEMO approval only. "
                "Nothing will be sent, booked, or changed.",
                value=False,
                key=f"consent_{patient_id}_{draft.id}",
            )
            approve, reject = st.columns(2)
            with approve:
                if st.button("Approve demo request", type="primary",
                             disabled=not consent, use_container_width=True):
                    updated = decide(draft, patient_id, "approve", consent=True)
                    st.session_state.care_draft = updated
                    st.session_state.care_history.append(audit_entry(updated,"approved_demo_only"))
                    st.rerun()
            with reject:
                if st.button("Reject request", use_container_width=True):
                    updated = decide(draft, patient_id, "reject")
                    st.session_state.care_draft = updated
                    st.session_state.care_history.append(audit_entry(updated,"rejected"))
                    st.rerun()
        elif draft.status == "approved_demo_only":
            st.success("Approved in this browser demo only. NOT sent or booked.")
        else:
            st.info("Request rejected. No action was taken.")

    st.markdown("#### Activity log")
    st.caption("In-memory demo events for this selected patient and browser session. "
               "They disappear when you switch patients or reload the server. "
               "The log intentionally excludes free-text health details.")
    history = st.session_state.get("care_history",[])
    if history:
        st.dataframe(history,use_container_width=True,hide_index=True)
        st.download_button("Download demo audit log (JSON)",
                           json.dumps(history,indent=2),
                           file_name=f"patientpilot-demo-audit-{patient_id}.json",
                           mime="application/json")
    else:
        st.info("No demo actions recorded for this patient yet.")
