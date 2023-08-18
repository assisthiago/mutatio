from django.contrib.auth.models import User
from django.test import TestCase

from app.employer.models import Employer


class ModelTest(TestCase):
    def setUp(self) -> None:
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
