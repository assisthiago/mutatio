from datetime import date
from unittest.mock import Mock

from django.contrib import messages
from django.test import TestCase

from app.patient.models import Diagnosis, Patient, Room
from app.report.admin import ReportAdmin, admin
from app.report.forms import ReportForm
from app.report.models import Report


class ModelTest(TestCase):
    def setUp(self):
        diagnosis = Diagnosis.objects.create(name="disease test")
        patient = Patient(
            name="patient test",
            age=99,
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            room=Room.objects.create(ward="A", bed=1),
        )

        patient.save()
        patient.diagnoses.set([diagnosis])

        self.report = Report.objects.create(
            ventilation_mode="",
            initial_nutritional_route="",
            actual_nutritional_route="",
            treatment="",
            conduct="",
            patient=patient,
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
        diagnosis = Diagnosis.objects.create(name="disease test")
        patient = Patient(
            name="patient test",
            age=99,
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            room=Room.objects.create(ward="A", bed=1),
        )

        patient.save()
        patient.diagnoses.set([diagnosis])

        Report.objects.create(
            ventilation_mode="",
            initial_nutritional_route="",
            actual_nutritional_route="",
            treatment="",
            conduct="",
            patient=patient,
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
        diagnosis = Diagnosis.objects.create(name="disease test")
        patient = Patient(
            name="patient test",
            age=99,
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            room=Room.objects.create(ward="A", bed=1),
        )

        patient.save()
        patient.diagnoses.set([diagnosis])

        Report.objects.create(
            ventilation_mode="ventilation_mode",
            initial_nutritional_route="ventilation_mode",
            actual_nutritional_route="ventilation_mode",
            treatment="ventilation_mode",
            conduct="ventilation_mode",
            patient=patient,
        )

        self.form = ReportForm(
            dict(
                ventilation_mode="ventilation_mode",
                initial_nutritional_route="initial_nutritional_route",
                actual_nutritional_route="actual_nutritional_route",
                treatment="treatment",
                conduct="conduct",
                observation="observation",
                patient=patient,
            )
        )

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

    def test_validation_error(self):
        self.form.is_valid()
        self.assertEqual(
            "Paciente Patient Test já registrado em um relatório para o dia de hoje.",
            self.form.errors.as_data().get("__all__")[0].message,
        )


class AdminTest(TestCase):
    fixtures = ["test_fixtures.json"]

    def setUp(self):
        self.model_admin = ReportAdmin(Report, admin.site)
        self.obj = Report.objects.first()

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)

    def test_get_shift(self):
        expected = self.model_admin.get_shift(self.obj)
        self.assertEqual(str(self.obj), expected)

    def test_get_patient(self):
        expected = self.model_admin.get_patient(self.model_admin.model.objects.first())
        self.assertEqual(
            f"<a href='/admin/patient/patient/{self.obj.patient.id}/change/'>{self.obj.patient}</a>",
            expected,
        )

    def test_has_changelist_actions(self):
        self.assertIn("copy_previous_reports", self.model_admin.changelist_actions)

    def test_copy_previous_reports(self):
        mock = self._call_action()
        mock.assert_called_once_with(
            None, "2 relatórios copiados com sucesso.", messages.SUCCESS
        )

    def test_copy_previous_reports_from_today(self):
        Report.objects.create(
            ventilation_mode="",
            initial_nutritional_route="",
            actual_nutritional_route="",
            treatment="",
            conduct="",
            patient=Patient.objects.first(),
        )

        mock = self._call_action()
        mock.assert_called_once_with(
            None, "Existe 1 relatório cadastrado para o dia de hoje.", messages.WARNING
        )

    def test_copy_previous_reports_empty(self):
        Report.objects.all().delete()
        mock = self._call_action()
        mock.assert_called_once_with(
            None, "Nenhum relatório foi encontrado.", messages.WARNING
        )

    def _call_action(self):
        mock = Mock()
        message_user = ReportAdmin.message_user
        ReportAdmin.message_user = mock
        self.model_admin.copy_previous_reports(None, None)
        ReportAdmin.message_user = message_user

        return mock
