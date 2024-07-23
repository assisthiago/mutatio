from django.test import TestCase

from app.patient.models import Patient
from app.report.models import Report


class ModelTest(TestCase):

    fixtures = ["auth", "patient", "report"]

    def setUp(self):
        self.report = Report.objects.first()

    def test_create(self):
        self.assertTrue(Report.objects.exists())

    def test_has_patient(self):
        self.assertTrue(self.report.patient)

    def test_patient(self):
        self.assertIsInstance(self.report.patient, Patient)

    def test_str(self):
        self.assertEqual(str(self.report), self.report.created_at.strftime("%Y%m%d"))
