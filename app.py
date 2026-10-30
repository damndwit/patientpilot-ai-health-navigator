"""PatientPilot AI — Milestone 1: synthetic patient record dashboard."""
import streamlit as st
from assistant import answer_question
from care_ui import render_care_actions
from records import load_bundle, resources, patient_records, label, date_of, patient_name, plain_search

st.set_page_config(page_title="PatientPilot AI | Demo",page_icon="🩺",layout="wide")
st.markdown("""<style>
.block-container {max-width:1180px;padding-top:2rem}
.hero {padding:24px;border-radius:18px;background:linear-gradient(120deg,#103a4f,#154e5c);color:white;margin-bottom:20px}
.hero h1 {color:white;margin:0;font-size:2rem}.hero p {color:#d8f4f8;margin:5px 0}
.tag {display:inline-block;padding:5px 10px;border-radius:12px;background:#29485c;font-size:.8rem}
</style>""",unsafe_allow_html=True)

bundle=load_bundle()
patients=resources(bundle,"Patient")
options={p["id"]:patient_name(p) for p in patients}
with st.sidebar:
    st.header("🩺 PatientPilot")
    st.caption("Synthetic healthcare demonstration")
    selected=st.selectbox("View demo patient",list(options),format_func=lambda x:options[x])
    st.divider()
    st.info("All records are fictional. No connection to real providers, pharmacies, insurers or patients.")
    st.caption("Care Actions offers simulated drafts and approval. No live healthcare integrations.")

person=next(p for p in patients if p["id"]==selected)
records=patient_records(bundle,selected)
def select(kind):return [x for x in records if x.get("resourceType")==kind]
st.markdown(f'<div class="hero"><div class="tag">DEMO MODE · SYNTHETIC PATIENT</div><h1>Welcome, {patient_name(person).split()[0]}</h1><p>Your records, care tasks and information in one place.</p></div>',unsafe_allow_html=True)
st.caption(f"Currently viewing: {patient_name(person)} · Fictional ID: {selected} · DOB: {person.get('birthDate','Not recorded')}")
st.subheader("💬 Ask PatientPilot AI")
st.caption("Search the selected fictional patient's record. Source citations are included. Optional Gemini answers require an API key; without one, local evidence-based answers still work.")
if "chat_patient" not in st.session_state or st.session_state.chat_patient != selected:
    st.session_state.chat_patient = selected
    st.session_state.chat_history = []

try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except (FileNotFoundError, KeyError):
    api_key = ""
with st.sidebar:
    st.caption("Assistant mode: " + ("Gemini AI + record retrieval" if api_key else "Local record lookup (no API key)"))

suggested = ["What was my last cholesterol result?", "What medications are in my records?", "When is my next appointment?", "What insurance is listed?"]
quick = st.columns(2)
for i, prompt_example in enumerate(suggested):
    with quick[i % 2]:
        if st.button(prompt_example, key=f"ask_{selected}_{i}", use_container_width=True):
            st.session_state.pending_question = prompt_example

with st.container(border=True):
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    typed = st.chat_input("Ask about my records, medications, appointments...")
    question = typed or st.session_state.pop("pending_question", None)
    if question:
        with st.chat_message("user"):
            st.write(question)
        answer = answer_question(bundle, selected, question, api_key=api_key)
        with st.chat_message("assistant"):
            st.markdown(answer.text)
            st.caption("Mode: " + answer.mode)
        st.session_state.chat_history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer.text},
        ])
st.divider()
c1,c2,c3,c4=st.columns(4)
c1.metric("Recorded conditions",len(select("Condition")))
c2.metric("Medications",len(select("MedicationRequest")))
c3.metric("Lab results",len(select("Observation")))
c4.metric("Appointments",len(select("Appointment")))

tabs=st.tabs(["🏠 Overview","🧪 Labs & reports","💊 Medications","📅 Appointments","🛡️ Insurance","🔎 Record search","🚑 Contacts","🧾 Care Actions"])
with tabs[0]:
    left,right=st.columns(2)
    with left:
        st.subheader("Conditions")
        for r in select("Condition"):st.write("•",label(r))
        st.subheader("Allergies")
        for r in select("AllergyIntolerance"):st.write("•",label(r))
    with right:
        st.subheader("Recent visit")
        for r in select("Encounter"):st.write("•",date_of(r),r.get("reasonCode",[{}])[0].get("text","Visit"))
        st.subheader("Care team")
        st.write("Cedar Grove Family Clinic (fictional)")
        st.caption("No real clinical system connected.")
with tabs[1]:
    st.subheader("Lab results")
    for r in sorted(select("Observation"),key=date_of,reverse=True):
        q=r.get("valueQuantity",{})
        st.write(f"**{label(r)}:** {q.get('value','—')} {q.get('unit','')} · {date_of(r)}")
    st.subheader("Reports")
    for r in select("DiagnosticReport"):
        with st.expander(f"{label(r)} · {date_of(r)}"):
            st.write(r.get("conclusion","No summary recorded"))
            st.caption(f"Record ID: {r['id']}")
    st.warning("Sample lab values are not interpreted for medical decisions.")
with tabs[2]:
    st.subheader("Medication records")
    for r in select("MedicationRequest"):
        st.write(f"**{label(r)}** — {r.get('status','unknown')} · recorded {date_of(r)}")
        st.caption(r.get("dosageInstruction",[{}])[0].get("text",""))
    st.info("Prescription refill requests will be an approval-controlled simulated workflow in a future milestone.")
with tabs[3]:
    st.subheader("Appointments")
    for r in select("Appointment"):
        st.write(f"**{label(r)}** · {r.get('start','')[:16].replace('T',' at ')} · {r.get('status','')}")
    st.info("These visits are fictional. Booking, rescheduling and clinic messages are not enabled.")
with tabs[4]:
    st.subheader("Coverage")
    for r in select("Coverage"):
        st.write("**Insurer:**",r.get("payor",[{}])[0].get("display","Not available"))
        st.write("**Plan:**",r.get("class",[{}])[0].get("name","Not available"))
        st.write("**Status:**",r.get("status",""))
    st.warning("Coverage details are fictional and cannot verify real benefits or claims.")
with tabs[5]:
    st.subheader("Search this patient's records")
    query=st.text_input("Try: cholesterol, refill, follow-up, allergy","")
    st.caption("Raw keyword lookup. For conversational answers use Ask PatientPilot AI above.")
    if query.strip():
        found=plain_search(records,query)
        if not found:st.info("No matching demo records. Try another keyword.")
        for r in found[:15]:
            with st.expander(f"{label(r)} — {r['resourceType']}"):
                st.write("Date:",date_of(r) or "Not recorded")
                st.code(f"{r['resourceType']}/{r['id']}")
                st.json(r,expanded=False)
with tabs[6]:
    st.subheader("Emergency contacts")
    for r in person.get("contact",[]):
        n=r.get("name",{})
        st.write("**Name:**"," ".join([*n.get("given",[]),n.get("family","")]))
        st.write("**Phone:**",r.get("telecom",[{}])[0].get("value","Not recorded"))
    st.warning("Sample phone numbers are placeholders. This application cannot contact emergency services.")
with tabs[7]:
    render_care_actions(bundle, selected, api_key)
st.divider()
st.caption("PatientPilot AI — portfolio prototype. All patient records and organizations are fictional. Not for diagnosis, treatment, or emergencies.")
