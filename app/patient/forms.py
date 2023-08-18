import re

from django import forms
from django.core.exceptions import ValidationError

from app.patient.models import Patient


def validate_isdigit(value):
    if not re.match("[0-9]", str(value)):
        raise ValidationError("Deve ter apenas dígitos.")

    return value


class PatientForm(forms.ModelForm):
    age = forms.IntegerField(
        label="Idade", validators=[validate_isdigit], widget=forms.TextInput
    )
    medical_record = forms.IntegerField(
        label="Prontuário", validators=[validate_isdigit], widget=forms.TextInput
    )

    class Meta:
        model = Patient
        fields = "__all__"
