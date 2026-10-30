import io
import json
import unittest
from fhir_sandbox import (
    FHIRSandboxError, get_capabilities, get_synthetic_patients,
    get_sample_observations,
)
from navigation import hospital_search_url, directions_url

class FakeResponse:
    def __init__(self, data):
        self.data = json.dumps(data).encode()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, n): return self.data[:n]

def mock_opener(result):
    return lambda request, timeout: FakeResponse(result)

class IntegrationTests(unittest.TestCase):
    def test_capabilities(self):
        data = {"resourceType": "CapabilityStatement", "fhirVersion": "4.0.1",
                "rest": [{"resource": [{"type": "Patient"}, {"type": "Observation"}]}]}
        response = get_capabilities(opener=mock_opener(data))
        self.assertIn("Patient", response["resource_types"])

    def test_patient_list(self):
        data = {"resourceType": "Bundle", "entry": [{"resource": {
            "resourceType": "Patient", "id": "synthetic1",
            "name": [{"given": ["Alex"], "family": "Test"}]}}]}
        result = get_synthetic_patients(opener=mock_opener(data))
        self.assertEqual(result[0]["name"], "Alex Test")

    def test_observation_patient_isolation(self):
        data = {"resourceType": "Bundle", "entry": [
            {"resource": {"resourceType": "Observation", "id": "good",
                          "subject": {"reference": "Patient/s1"}, "code": {"text": "Test"}}},
            {"resource": {"resourceType": "Observation", "id": "bad",
                          "subject": {"reference": "Patient/s2"}, "code": {"text": "Test"}}},
        ]}
        result = get_sample_observations("s1", opener=mock_opener(data))
        self.assertEqual([x["id"] for x in result], ["good"])

    def test_invalid_patient_identifier_rejected(self):
        with self.assertRaises(FHIRSandboxError):
            get_sample_observations("../../admin", opener=mock_opener({}))

    def test_hospital_search_url_encoded(self):
        url = hospital_search_url("Trenton, NJ")
        self.assertIn("Trenton", url)
        self.assertIn("hospitals", url)

    def test_directions_does_not_book(self):
        url = directions_url("Trenton, NJ", "123 Example Street")
        self.assertIn("maps/dir", url)
        self.assertIn("destination=", url)

if __name__ == "__main__":
    unittest.main()
