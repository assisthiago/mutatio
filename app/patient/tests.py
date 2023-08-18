from datetime import date

from django.test import TestCase

from app.patient.models import Diagnosis, Patient


class DiagnosisModelTest(TestCase):
    def setUp(self):
        self.diagnosis = Diagnosis(name="disease test")

    def test_str(self):
        self.assertEqual(str(self.diagnosis), "disease test")


class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            name="patient test",
            age=99,
            room="a1",
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            diagnosis=Diagnosis.objects.create(name="disease test"),
        )

    def test_create(self):
        self.assertTrue(Patient.objects.exists())

    def test_has_diagnosis(self):
        self.assertTrue(self.patient.diagnosis)

    def test_diagnosis(self):
        self.assertIsInstance(self.patient.diagnosis, Diagnosis)

    def test_str(self):
        self.assertEqual(str(self.patient), "Patient Test")
