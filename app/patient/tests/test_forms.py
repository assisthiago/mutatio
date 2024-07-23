from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from app.patient.forms import PatientForm, validate_isdigit
from app.patient.models import Diagnosis, Room


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
