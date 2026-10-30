import unittest
from assistant import answer_question, retrieve, offline_answer, safety_message
from records import load_bundle

class AssistantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.bundle=load_bundle()

    def test_alex_lab_search_has_citations(self):
        evidence=retrieve(self.bundle,"alex-demo","What was my latest cholesterol lab?")
        self.assertTrue(evidence)
        self.assertTrue(any(i.identifier=="Observation/obs-alex-chol-2" for i in evidence))
        self.assertIn("[Observation/obs-alex-chol-2]",offline_answer(evidence).text)

    def test_patients_records_are_isolated(self):
        jamie=retrieve(self.bundle,"jamie-demo","cholesterol")
        self.assertTrue(jamie)
        self.assertTrue(all("alex" not in i.identifier for i in jamie))
        self.assertFalse(any(i.identifier=="Observation/obs-alex-chol-2" for i in jamie))

    def test_appointments_find_correct_record(self):
        r=retrieve(self.bundle,"jamie-demo","When is my next appointment?")
        self.assertTrue(any(i.identifier=="Appointment/appt-jamie-1" for i in r))

    def test_insurance_lookup(self):
        r=retrieve(self.bundle,"alex-demo","What insurance do I have?")
        self.assertTrue(any(i.identifier=="Coverage/cov-alex" for i in r))

    def test_no_evidence_does_not_guess(self):
        a=answer_question(self.bundle,"alex-demo","Is my pet dragon insured?")
        self.assertNotEqual(a.mode,"Gemini LLM")
        self.assertIn("couldn't find",a.text)

    def test_medication_advice_blocked(self):
        self.assertIsNotNone(safety_message("Should I stop my medication?"))
        a=answer_question(self.bundle,"alex-demo","Should I stop my medication?")
        self.assertFalse(a.evidence)
        self.assertIn("clinician",a.text)

    def test_emergency_message(self):
        a=answer_question(self.bundle,"alex-demo","I have chest pain")
        self.assertIn("emergency",a.text)

    def test_offline_no_key(self):
        a=answer_question(self.bundle,"alex-demo","What is my prescription?")
        self.assertEqual(a.mode,"record lookup")
        self.assertTrue(any(i.identifier.startswith("MedicationRequest/") for i in a.evidence))

if __name__=="__main__":unittest.main()
