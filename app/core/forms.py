from django import forms
from django.contrib.auth.password_validation import validate_password


class SignInForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field in ("username", "password"):
                self.fields[field].widget.attrs.update(
                    {"class": "form-control", "placeholder": field}
                )
