from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        response = self.client.post(reverse("logout"))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
