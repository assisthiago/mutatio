from django.test import TestCase
from django.utils import timezone

from app.patient.models import Patient
from app.report.forms import ReportForm
from app.report.models import Report


class FormTest(TestCase):

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

        self.form = ReportForm(
            dict(
                ventilation_mode="Ar ambiente",
                initial_nutritional_route="Sonda",
                actual_nutritional_route="Via oral",
                treatment="Sim",
                conduct="Via oral.",
                observation="Mais sonda.",
                patient=Patient.objects.first(),
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
            "Paciente João Silva já registrado em um relatório para o dia de hoje.",
            self.form.errors.as_data().get("__all__")[0].message,
        )
