from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase


class ReportsListViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="user.test", password="zbbc9fi0h!")
        self.client.login(username="user.test", password="zbbc9fi0h!")
        self.resp = self.client.get(r("reports-list"))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "reports-list.html")


class ReportsDetailViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="user.test", password="zbbc9fi0h!")
        self.client.login(username="user.test", password="zbbc9fi0h!")
        self.resp = self.client.get(r("reports-detail", pk=1))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)
