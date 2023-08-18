from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from app.employer.admin import EmployerAdmin, admin
from app.employer.forms import EmployerForm, validate_phone
from app.employer.models import Employer


class ModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="user@test.com",
            password="zbbc9fi0h!",
            email="user@test.com",
            first_name="user",
            last_name="test",
        )

        self.employer = Employer.objects.create(user=user, phone="21996643040")

    def test_create(self):
        self.assertTrue(Employer.objects.exists())

    def test_has_user(self):
        self.assertTrue(self.employer.user)

    def test_user(self):
        self.assertIsInstance(self.employer.user, User)

    def test_str(self):
        self.assertEqual(str(self.employer), "User Test")


class FormTest(TestCase):
    def setUp(self):
        self.form = EmployerForm()

    def test_form_has_fields(self):
        expected = ["user", "phone"]
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_form_has_validators(self):
        self.assertIn(validate_phone, self.form.fields["phone"].validators)

    def test_validate_phone(self):
        self.assertTrue(validate_phone("21999999999"))

    def test_validate_phone_invalid(self):
        with self.assertRaises(ValidationError):
            validate_phone("2I999999999")


class AdminTest(TestCase):
    def setUp(self):
        self.admin = EmployerAdmin(Employer, admin.site)

    def test_has_form(self):
        self.assertTrue(self.admin.form)
