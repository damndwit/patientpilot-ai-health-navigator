"""Permission and patient scoping tests for local care action simulations."""
import unittest

from records import load_bundle
from workflows import (
    ACTION_TYPES, OUTBOUND_MESSAGE, audit_entry, create_draft, decide,
    draft_summary, medications_for, suggest_kind,
)

class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = load_bundle()

    def test_all_intents_detected_without_llm(self):
        cases = {
            "Can you book my appointment?": "appointment_request",
            "I need a refill of my medicine": "refill_inquiry",
            "Ask my insurer about my claim": "insurance_message",
            "Message the clinic about a question": "clinic_message",
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(suggest_kind(phrase)[0], expected)
        self.assertIsNone(suggest_kind("What is the capital of France?")[0])

    def test_emergencies_do_not_suggest_action(self):
        self.assertIsNone(suggest_kind("I have chest pain")[0])
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "alex-demo", "clinic_message",
                         "I have chest pain, please book now")

    def test_appointment_is_pending_not_booked(self):
        draft = create_draft(self.bundle, "alex-demo", "appointment_request",
                             "Request a routine appointment", "2026-12-10")
        self.assertEqual(draft.status, "pending_review")
        self.assertEqual(draft.recipient, "Cedar Grove Family Clinic (fictional)")
        self.assertIn("Sends nothing", draft_summary(draft)["What approval does"])
        self.assertEqual(draft.preferred_date, "2026-12-10")

    def test_refill_requires_medication_in_selected_patient(self):
        alex = medications_for(self.bundle, "alex-demo")
        self.assertTrue(alex)
        medref = "MedicationRequest/" + alex[0]["id"]
        draft = create_draft(self.bundle, "alex-demo", "refill_inquiry",
                             "Ask clinic whether a refill is available", medication_ref=medref)
        self.assertEqual(draft.related_record, medref)
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "jamie-demo", "refill_inquiry",
                         "Ask about a refill", medication_ref=medref)

    def test_insurer_uses_selected_patient(self):
        a = create_draft(self.bundle, "alex-demo", "insurance_message",
                         "Please explain the sample coverage")
        self.assertEqual(a.related_record, "Coverage/cov-alex")
        b = create_draft(self.bundle, "jamie-demo", "insurance_message",
                         "Please explain the sample coverage")
        self.assertEqual(b.related_record, "Coverage/cov-jamie")

    def test_approval_requires_consent_and_patient_match(self):
        draft = create_draft(self.bundle, "alex-demo", "clinic_message",
                             "Question about my upcoming appointment")
        with self.assertRaises(PermissionError):
            decide(draft, "alex-demo", "approve")
        with self.assertRaises(PermissionError):
            decide(draft, "jamie-demo", "approve", consent=True)
        updated = decide(draft, "alex-demo", "approve", consent=True)
        self.assertEqual(updated.status, "approved_demo_only")
        self.assertEqual(audit_entry(updated, "approved_demo_only")["result"], OUTBOUND_MESSAGE)
        with self.assertRaises(ValueError):
            decide(updated, "alex-demo", "approve", consent=True)

    def test_reject_and_audit(self):
        draft = create_draft(self.bundle, "alex-demo", "clinic_message",
                             "Ask for clinic office hours")
        rejected = decide(draft, "alex-demo", "reject")
        self.assertEqual(rejected.status, "rejected")
        log = audit_entry(rejected, "rejected")
        self.assertEqual(log["event"], "rejected")
        self.assertNotIn("Ask for clinic office hours", str(log))

    def test_invalid_types_dates_and_inputs(self):
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "alex-demo", "send_real_prescription", "Request")
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "invalid_patient", "clinic_message", "A short request")
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "alex-demo", "appointment_request",
                         "A short request", preferred_date="not-a-date")
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "alex-demo", "clinic_message", "x")
        with self.assertRaises(ValueError):
            create_draft(self.bundle, "alex-demo", "clinic_message",
                         "A short request", medication_ref="MedicationRequest/med-alex-1")

if __name__ == "__main__":
    unittest.main()
