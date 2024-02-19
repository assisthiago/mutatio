from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from app.core.forms import SignInForm


class SignInGetViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("sign-in"))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "sign-in.html")

    def test_html(self):
        tags = (
            ("<form", 1),
            ("<input", 3),
            ('type="hidden"', 1),
            ('type="text"', 1),
            ('type="password"', 1),
            ('type="submit"', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.resp.context["form"]
        self.assertIsInstance(form, SignInForm)


class SignInPostViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="user.test", password="zbbc9fi0h!")

    def test_post(self):
        resp = self.client.post(r("sign-in"), self._make_data())
        self.assertEqual(302, resp.status_code)

    def test_user_logged_in(self):
        self.client.post(r("sign-in"), self._make_data())
        user = User.objects.first()
        self.assertTrue(user.is_authenticated)

    def _make_data(self, **kwargs):
        data = dict(
            username="user.test",
            password="zbbc9fi0h!",
        )

        return dict(data, **kwargs)


class SignInInvalidPostTest(TestCase):
    def setUp(self):
        self.resp = self.client.post(
            r("sign-in"),
            {
                "username": "invalid.test",
                "password": "zbbc9fi0h!",
            },
        )

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_html_alert_message(self):
        tags = (
            ('<div id="message-alert"', 1),
            ("<span>Verifique seus dados.</span>", 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
