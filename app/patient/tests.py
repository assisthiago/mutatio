from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.patient.admin import PatientAdmin, admin
from app.patient.forms import PatientForm, validate_isdigit
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
            nutritional_route="",
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

    def test_admin_url(self):
        self.assertEqual(
            "/admin/patient/patient/1/change/", self.patient.get_admin_url()
        )


class FormTest(TestCase):
    def setUp(self):
        self.form = PatientForm()

    def test_form_has_fields(self):
        expected = [
            "name",
            "age",
            "room",
            "medical_record",
            "hospitalized_in",
            "sorted_in",
            "nutritional_route",
            "released",
            "diagnosis",
        ]

        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_validate_isdigit(self):
        self.assertTrue(validate_isdigit("1"))

    def test_validate_isdigit_invalid(self):
        with self.assertRaises(ValidationError):
            validate_isdigit("I")


class AdminTest(TestCase):
    def setUp(self):
        self.model_admin = PatientAdmin(Patient, admin.site)
        Patient.objects.create(
            name="patient test",
            age=99,
            room="a1",
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            diagnosis=Diagnosis.objects.create(name="disease test"),
        )

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)
