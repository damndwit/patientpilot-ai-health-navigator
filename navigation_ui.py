"""Streamlit read-only FHIR sandbox and care navigation views."""
import streamlit as st
from fhir_sandbox import (
    FHIRSandboxError, get_capabilities, get_synthetic_patients,
    get_sample_observations, BASE_URL,
)
from navigation import hospital_search_url, directions_url, clinic_destination
from records import patient_name, patient_records, label

@st.cache_data(ttl=120, show_spinner=False)
def capability_data():
    return get_capabilities()

@st.cache_data(ttl=120, show_spinner=False)
def demo_patients():
    return get_synthetic_patients()

@st.cache_data(ttl=120, show_spinner=False)
def sample_labs(pid):
    return get_sample_observations(pid)

def render_fhir_explorer():
    st.subheader("🔗 FHIR R4 Sandbox Explorer")
    st.info("This is a separate read-only public TEST server. Its synthetic patients are not your selected PatientPilot demo patient. Do not enter any real patient identifiers here.")
    st.caption("SMART Health IT public R4 test endpoint: " + BASE_URL)
    if st.button("Check FHIR server", key="check_cap"):
        try:
            info = capability_data()
            st.success(f"Connected: FHIR {info['fhir_version']} · {len(info['resource_types'])} resource types advertised")
            st.write("Supported types (sample):", ", ".join(info["resource_types"][:18]))
        except FHIRSandboxError as exc:
            st.error(str(exc))
    if st.button("Load up to 5 sandbox test patients", key="fetch_sandbox"):
        try:
            st.session_state.sandbox_patients = demo_patients()
        except FHIRSandboxError as exc:
            st.error(str(exc))
    records = st.session_state.get("sandbox_patients", [])
    if records:
        choices = {p["id"]: f'{p["name"]} · {p["id"]}' for p in records}
        choice = st.selectbox("Sandbox patient (not the local demo patient)", list(choices), format_func=choices.get)
        if st.button("View up to 5 test lab observations", key="fetch_labs"):
            try:
                items = sample_labs(choice)
                if items:
                    st.dataframe(items, use_container_width=True, hide_index=True)
                else:
                    st.info("No observations returned for this synthetic sandbox patient.")
            except FHIRSandboxError as exc:
                st.error(str(exc))
    st.warning("Public sandbox results can change or be unavailable. This read-only demo does not log in, update records, or establish healthcare provider access.")

def render_care_navigation(person, local_records):
    st.subheader("🧭 Care Navigation")
    st.info("Directory links and trip planning only. No transportation, clinic, or emergency services are booked or contacted.")
    st.markdown("#### Find nearby hospitals")
    area = st.text_input("Enter a city, state, or ZIP code", key="hospital_area", placeholder="Trenton, NJ")
    if area:
        try:
            st.link_button("Search hospitals in Google Maps ↗", hospital_search_url(area))
        except ValueError as exc:
            st.warning(str(exc))
    st.caption("This opens a public map search, not a verified list of in-network or currently available hospitals.")
    st.markdown("#### Plan travel to an appointment")
    appointments = [r for r in local_records if r.get("resourceType") == "Appointment"]
    for item in appointments:
        st.write(f'**Demo appointment:** {label(item)} — {item.get("start", "")[:16].replace("T", " at ")}')
    st.caption(clinic_destination())
    with st.form("trip_planner"):
        origin = st.text_input("Starting point (city or address)", placeholder="Trenton, NJ")
        destination = st.text_input("Real destination address (enter manually)", placeholder="Clinic's actual address")
        submitted = st.form_submit_button("Prepare driving directions")
    if submitted:
        try:
            route = directions_url(origin, destination)
            st.session_state.navigation_link = route
            st.success("Directions link prepared. No ride has been ordered.")
        except ValueError as exc:
            st.error(str(exc))
    if st.session_state.get("navigation_link"):
        st.link_button("Open driving directions ↗", st.session_state.navigation_link)
    st.markdown("#### Emergency contact on demo record")
    for contact in person.get("contact", []):
        name = contact.get("name", {})
        text = " ".join([*name.get("given", []), name.get("family", "")])
        phone = contact.get("telecom", [{}])[0].get("value", "Not recorded")
        st.write(f"**{text}** · {phone} (fictional)")
    st.warning("For an actual emergency, call local emergency services. This app cannot contact them.")
