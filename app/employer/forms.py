from django import forms

from app.employer.models import Employer


class EmployerForm(forms.ModelForm):
    phone = forms.IntegerField(widget=forms.TextInput)

    class Meta:
        model = Employer
        fields = ["user", "phone"]
