"""Read-only connection to SMART Health IT's PUBLIC synthetic FHIR R4 test server.

No authentication, no writes, no patient data uploads. Never connect real records
or credentials to public sandboxes. Remote data is kept separate from demo charts.
"""
from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://r4.smarthealthit.org"
MAX_BYTES = 2_000_000
TIMEOUT_SECONDS = 8

class FHIRSandboxError(Exception):
    """Friendly error for unavailable or unexpected sandbox responses."""


def _get(resource: str, params: dict | None = None, opener=urlopen) -> dict:
    if resource not in {"metadata", "Patient", "Observation"}:
        raise FHIRSandboxError("This demo permits read-only metadata, Patient and Observation requests.")
    path = BASE_URL + "/" + resource
    if params:
        path += "?" + urlencode(params)
    request = Request(path, headers={"Accept": "application/fhir+json",
                                    "User-Agent": "PatientPilot-Learning-Demo/1.0"},
                      method="GET")
    try:
        with opener(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise FHIRSandboxError("The test server sent too much data.")
        result = json.loads(raw.decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, UnicodeError) as exc:
        raise FHIRSandboxError("The public FHIR test server is unavailable or returned an invalid response.") from exc
    if not isinstance(result, dict):
        raise FHIRSandboxError("Expected a FHIR JSON object.")
    if result.get("resourceType") == "OperationOutcome":
        raise FHIRSandboxError("The public FHIR server rejected this test query.")
    return result


def get_capabilities(opener=urlopen) -> dict:
    statement = _get("metadata", opener=opener)
    if statement.get("resourceType") != "CapabilityStatement":
        raise FHIRSandboxError("Expected a FHIR CapabilityStatement.")
    kinds = sorted({r.get("type") for rest in statement.get("rest", [])
                    for r in rest.get("resource", []) if r.get("type")})
    return {
        "server": BASE_URL,
        "fhir_version": statement.get("fhirVersion", "unknown"),
        "software": statement.get("software", {}).get("name", "unknown"),
        "resource_types": kinds,
    }


def get_synthetic_patients(opener=urlopen) -> list[dict]:
    bundle = _get("Patient", {"_count": "5"}, opener=opener)
    if bundle.get("resourceType") != "Bundle":
        raise FHIRSandboxError("Expected a FHIR search Bundle.")
    out = []
    for entry in bundle.get("entry", [])[:5]:
        patient = entry.get("resource", {})
        if patient.get("resourceType") != "Patient":
            continue
        pid = str(patient.get("id", ""))
        if not re.fullmatch(r"[A-Za-z0-9\-.]{1,64}", pid):
            continue
        name = patient.get("name", [{}])[0] if patient.get("name") else {}
        display = " ".join([*name.get("given", []), name.get("family", "")]).strip()
        out.append({"id": pid, "name": display or "Unnamed sandbox patient",
                    "gender": patient.get("gender", "unknown")})
    return out


def get_sample_observations(patient_id: str, opener=urlopen) -> list[dict]:
    if not re.fullmatch(r"[A-Za-z0-9\-.]{1,64}", patient_id):
        raise FHIRSandboxError("Invalid sandbox patient ID.")
    bundle = _get("Observation", {"patient": patient_id, "_count": "5"}, opener=opener)
    if bundle.get("resourceType") != "Bundle":
        raise FHIRSandboxError("Expected a FHIR search Bundle.")
    out = []
    for entry in bundle.get("entry", [])[:5]:
        observation = entry.get("resource", {})
        if observation.get("resourceType") != "Observation":
            continue
        # Only show records whose subject explicitly matches the sandbox patient.
        if observation.get("subject", {}).get("reference", "").split("/")[-1] != patient_id:
            continue
        code = observation.get("code", {})
        coding = code.get("coding", [])
        name = code.get("text") or (coding[0].get("display", "") if coding else "Observation")
        quantity = observation.get("valueQuantity") or {}
        out.append({
            "id": str(observation.get("id", "unknown"))[:80],
            "name": str(name)[:120],
            "date": (observation.get("effectiveDateTime") or
                     observation.get("issued") or "")[:10],
            "value": str(quantity.get("value", "Not available"))[:40],
            "unit": str(quantity.get("unit", ""))[:30],
        })
    return out
