import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

    def clean_room(self):
        data = self.cleaned_data["room"]

        try:
            if not self.instance.id and data.patient:
                raise ValidationError(f"Quarto encontra-se ocupado.")

        except ObjectDoesNotExist:
            pass

        return data

    class Meta:
        model = Patient
        fields = "__all__"
