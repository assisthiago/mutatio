from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from app.employer.models import Employer
from app.patient.models import Diagnosis, Patient
from app.report.admin import ReportAdmin, admin
from app.report.forms import ReportForm
from app.report.models import Report


class ModelTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            ventilation_mode="",
            initial_nutritional_route="",
            actual_nutritional_route="",
            treatment="",
            conduct="",
            patient=Patient.objects.create(
                name="patient test",
                age=99,
                room="a1",
                medical_record="1",
                hospitalized_in=date.today(),
                sorted_in=date.today(),
                diagnosis=Diagnosis.objects.create(name="disease test"),
            ),
        )

    def test_create(self):
        self.assertTrue(Report.objects.exists())

    def test_has_patient(self):
        self.assertTrue(self.report.patient)

    def test_patient(self):
        self.assertIsInstance(self.report.patient, Patient)

    def test_str(self):
        self.assertEqual(
            str(self.report), f"Relatório {self.report.created_at.strftime('%Y%m%d')}"
        )


class FormTest(TestCase):
    def setUp(self):
        self.form = ReportForm()

    def test_form_has_fields(self):
        expected = [
            "ventilation_mode",
            "initial_nutritional_route",
            "actual_nutritional_route",
            "treatment",
            "conduct",
            "observation",
            "patient",
        ]
        self.assertSequenceEqual(expected, list(self.form.fields))


class AdminTest(TestCase):
    def setUp(self):
        self.model_admin = ReportAdmin(Report, admin.site)

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)
