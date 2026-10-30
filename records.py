"""Small read-only parser for the repository's fictional FHIR-style demo bundle."""
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "synthetic_fhir_bundle.json"

def load_bundle(path=DATA_PATH):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("resourceType") != "Bundle":
        raise ValueError("Expected a FHIR-style Bundle")
    return data

def resources(bundle, kind=None):
    values = [entry["resource"] for entry in bundle.get("entry", [])]
    return [r for r in values if kind is None or r.get("resourceType") == kind]

def patient_records(bundle, patient_id):
    target = f"Patient/{patient_id}"
    result = []
    for item in resources(bundle):
        if item.get("subject", {}).get("reference") == target or item.get("patient", {}).get("reference") == target or item.get("beneficiary", {}).get("reference") == target:
            result.append(item)
        elif item.get("resourceType") == "Appointment" and any(p.get("actor",{}).get("reference") == target for p in item.get("participant",[])):
            result.append(item)
    return result

def label(resource):
    for field in ("code", "medicationCodeableConcept"):
        value = resource.get(field)
        if value:
            return value.get("text") or value.get("coding", [{}])[0].get("display", "")
    return resource.get("description") or resource.get("resourceType","Unknown")

def date_of(resource):
    return (resource.get("effectiveDateTime") or resource.get("start") or resource.get("authoredOn") or resource.get("onsetDateTime") or resource.get("period",{}).get("start") or "")[:10]

def patient_name(patient):
    n = patient.get("name",[{}])[0]
    return " ".join([*n.get("given",[]),n.get("family","")]).strip()

def plain_search(items, query):
    """Simple keyword search across demo records; does not use AI."""
    tokens = [t.casefold() for t in query.split() if len(t)>1]
    if not tokens:
        return []
    scored=[]
    for r in items:
        indexed = " ".join([label(r),r.get("conclusion",""),r.get("status",""),date_of(r),json.dumps(r,ensure_ascii=False)]).casefold()
        count=sum(t in indexed for t in tokens)
        if count:
            scored.append((count,r))
    return [r for _,r in sorted(scored,key=lambda x:x[0],reverse=True)]
