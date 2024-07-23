from django.test import TestCase

from app.patient.models import Diagnosis, Patient


class DiagnosisModelTest(TestCase):

    fixtures = ["auth", "patient"]

    def setUp(self):
        self.diagnosis = Diagnosis.objects.first()

    def test_str(self):
        self.assertEqual(str(self.diagnosis), "Tuberculose")


class PatientModelTest(TestCase):

    fixtures = ["auth", "patient"]

    def setUp(self):
        self.patient = Patient.objects.first()

    def test_has_diagnoses(self):
        self.assertTrue(self.patient.diagnoses)

    def test_diagnoses(self):
        self.assertIsInstance(self.patient.diagnoses.first(), Diagnosis)

    def test_str(self):
        self.assertEqual(str(self.patient), "João Silva")

    def test_admin_url(self):
        self.assertEqual(
            "/admin/patient/patient/1/change/", self.patient.get_admin_url()
        )
