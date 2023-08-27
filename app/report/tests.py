from datetime import date, datetime, timedelta
from unittest.mock import Mock

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
        self.assertEqual(str(self.report), self.report.created_at.strftime("%Y%m%d"))


class ManagerTest(TestCase):
    def setUp(self):
        Report.objects.create(
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

    def test_report_from_today(self):
        self.assertTrue(Report.objects.from_today().exists())

    def test_report_from_yesterday(self):
        self.assertFalse(Report.objects.from_yesterday().exists())

    def test_report_last_availables(self):
        self.assertTrue(Report.objects.last_availables().exists())

    def test_not_report_last_availables(self):
        Report.objects.all().delete()
        self.assertIsNone(Report.objects.last_availables())


class FormTest(TestCase):
    def setUp(self):
        self.form = ReportForm()

    def test_form_has_fields(self):
        expected = [
            "patient",
            "ventilation_mode",
            "initial_nutritional_route",
            "actual_nutritional_route",
            "treatment",
            "conduct",
            "observation",
        ]
        self.assertSequenceEqual(expected, list(self.form.fields))


class AdminTest(TestCase):
    def setUp(self):
        self.model_admin = ReportAdmin(Report, admin.site)
        Report.objects.create(
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

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)

    def test_get_shift(self):
        expected = self.model_admin.get_shift(self.model_admin.model.objects.first())
        self.assertEqual(date.today().strftime("%Y%m%d"), expected)

    def test_get_patient(self):
        expected = self.model_admin.get_patient(self.model_admin.model.objects.first())
        self.assertEqual(
            "<a href='/admin/patient/patient/1/change/'>Patient Test</a>", expected
        )

    def test_has_changelist_actions(self):
        self.assertIn("copy_previous_reports", self.model_admin.changelist_actions)
