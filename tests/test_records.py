import unittest
from records import load_bundle, resources, patient_records, plain_search, patient_name

class TestSyntheticRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=load_bundle()
    def test_bundle(self):self.assertEqual(self.data["resourceType"],"Bundle")
    def test_two_demo_patients(self):self.assertEqual(len(resources(self.data,"Patient")),2)
    def test_patients_have_distinct_records(self):
        a=patient_records(self.data,"alex-demo")
        b=patient_records(self.data,"jamie-demo")
        self.assertTrue(a and b)
        self.assertNotEqual({x["id"] for x in a},{x["id"] for x in b})
    def test_patient_name(self):self.assertEqual(patient_name(resources(self.data,"Patient")[0]),"Alex Morgan")
    def test_lab_search(self):
        records=patient_records(self.data,"alex-demo")
        self.assertTrue(any(r["resourceType"]=="Observation" for r in plain_search(records,"cholesterol")))
    def test_no_cross_patient_records(self):
        records=patient_records(self.data,"jamie-demo")
        self.assertTrue(all(x.get("subject",{}).get("reference")!="Patient/alex-demo" for x in records))
if __name__=="__main__":unittest.main()
