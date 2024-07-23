from django.test import TestCase

from app.patient.models import Patient
from app.report.models import Report


class ManagerTest(TestCase):

    fixtures = ["auth", "patient", "report"]

    def setUp(self):
        Report.objects.create(
            ventilation_mode="Ar ambiente",
            initial_nutritional_route="Sonda",
            actual_nutritional_route="Via oral",
            treatment="Sim",
            conduct="Via oral.",
            observation="Mais sonda.",
            patient=Patient.objects.first(),
        )

    def test_report_from_today(self):
        self.assertTrue(Report.objects.from_today().exists())

    def test_report_from_yesterday(self):
        self.assertFalse(Report.objects.from_yesterday().exists())

    def test_report_last_availables(self):
        self.assertTrue(Report.objects.last_availables().exists())

    def test_not_report_last_availables(self):
        Report.objects.all().delete()
        self.assertIsNone(Report.objects.last_availables())
