from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase


class SignOutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user.test", password="zbbc9fi0h!"
        )
        self.client.login(username="user.test", password="zbbc9fi0h!")
        self.resp = self.client.get(r("sign-out"))

    def test_get(self):
        self.assertEqual(302, self.resp.status_code)
