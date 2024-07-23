from django.test import TestCase

from app.patient.admin import PatientAdmin, RoomAdmin, admin
from app.patient.models import Patient, Room


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
