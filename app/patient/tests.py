from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.patient.admin import PatientAdmin, RoomAdmin, admin
from app.patient.forms import PatientForm, validate_isdigit
from app.patient.models import Diagnosis, Patient, Room


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


class PatientFormTest(TestCase):

    fixtures = ["auth", "patient"]

    def setUp(self):
        self.data = {
            "name": "Maria Silva",
            "age": 30,
            "medical_record": "1",
            "hospitalized_in": date.today(),
            "sorted_in": date.today(),
            "nutritional_route": "Via oral",
            "diagnoses": [Diagnosis.objects.first()],
            "room": Room.objects.first(),
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
            "diagnoses",
            "room",
        ]

        self.assertSequenceEqual(expected, list(PatientForm().fields))

    def test_validate_isdigit(self):
        self.assertTrue(validate_isdigit("1"))

    def test_validate_isdigit_invalid(self):
        with self.assertRaises(ValidationError):
            validate_isdigit("I")

    def test_is_valid(self):
        data = self.data
        data["room"] = Room.objects.create(ward="Aa", bed=2)
        self.assertTrue(PatientForm(data).is_valid())

    def test_is_not_valid(self):
        self.assertFalse(PatientForm({}).is_valid())

    def test_raised_error_clean_room(self):
        form = PatientForm()
        form.cleaned_data = dict(**self.data)

        with self.assertRaises(ValidationError):
            form.clean_room()


class PatientAdminTest(TestCase):

    fixtures = ["auth", "patient"]

    def setUp(self):
        self.model_admin = PatientAdmin(Patient, admin.site)

    def test_has_form(self):
        self.assertTrue(self.model_admin.form)

    def test_get_diagnoses(self):
        expected = self.model_admin.get_diagnoses(
            self.model_admin.model.objects.first()
        )
        self.assertEqual("Tuberculose", expected)


class RoomAdminTest(TestCase):

    fixtures = ["auth", "patient"]

    def setUp(self):
        self.model_admin = RoomAdmin(Patient, admin.site)

    def test_get_shift(self):
        expected = self.model_admin.see_more(self.model_admin.model.objects.first())
        self.assertEqual("Ver detalhes", expected)

    def test_str(self):
        self.assertEqual("Aa1", str(Room.objects.first()))
