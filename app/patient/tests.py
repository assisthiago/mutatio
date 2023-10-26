from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.patient.admin import PatientAdmin, RoomAdmin, admin
from app.patient.forms import PatientForm, validate_isdigit
from app.patient.models import Diagnosis, Patient, Room


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
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            nutritional_route="",
            diagnosis=Diagnosis.objects.create(name="disease test"),
            room=Room.objects.create(ward="A", bed=1),
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


class PatientFormTest(TestCase):
    def setUp(self) -> None:
        diagnosis = Diagnosis.objects.create(name="disease test")
        room = Room.objects.create(ward="A", bed=1)
        self.patient = {
            "name": "patient test",
            "age": 99,
            "medical_record": "1",
            "hospitalized_in": date.today(),
            "sorted_in": date.today(),
            "nutritional_route": "nutritional route test",
            "diagnosis": diagnosis,
            "room": room,
        }

    def test_form_has_fields(self):
        expected = [
            "name",
            "age",
            "medical_record",
            "hospitalized_in",
            "sorted_in",
            "nutritional_route",
            "eligible",
            "diagnosis",
            "room",
        ]

        self.assertSequenceEqual(expected, list(PatientForm().fields))

    def test_validate_isdigit(self):
        self.assertTrue(validate_isdigit("1"))

    def test_validate_isdigit_invalid(self):
        with self.assertRaises(ValidationError):
            validate_isdigit("I")

    def test_is_valid(self):
        self.assertTrue(PatientForm(self.patient).is_valid())

    def test_is_not_valid(self):
        self.assertFalse(PatientForm({}).is_valid())

    def test_raised_error_clean_room(self):
        Patient.objects.create(**self.patient)
        form = PatientForm()
        form.cleaned_data = dict(**self.patient)

        with self.assertRaises(ValidationError):
            form.clean_room()


class PatientAdminTest(TestCase):
    def setUp(self):
        self.model_admin = PatientAdmin(Patient, admin.site)
        Patient.objects.create(
            name="patient test",
            age=99,
            medical_record="1",
            hospitalized_in=date.today(),
            sorted_in=date.today(),
            diagnosis=Diagnosis.objects.create(name="disease test"),
            room=Room.objects.create(ward="A", bed=1),
        )

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)


class RoomAdminTest(TestCase):
    def setUp(self):
        self.model_admin = RoomAdmin(Patient, admin.site)
        Room.objects.create(ward="A", bed=1)

    def test_get_shift(self):
        expected = self.model_admin.see_more(self.model_admin.model.objects.first())
        self.assertEqual("Ver detalhes", expected)
