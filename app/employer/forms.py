import re

from django import forms
from django.core.exceptions import ValidationError

from app.employer.models import Employer


def validate_phone(value):
    if not re.match("[0-9]{11}", value):
        raise ValidationError("Deve ter 11 dígitos.")

    return value


class EmployerForm(forms.ModelForm):
    phone = forms.IntegerField(
        label="telefone", validators=[validate_phone], widget=forms.TextInput
    )

    class Meta:
        model = Employer
        fields = ["user", "phone"]
