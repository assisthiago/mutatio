from django import forms
from django.core.exceptions import ValidationError

from app.report.models import Report


class ReportForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        patient = cleaned_data.get("patient")

        if not self.instance.id and Report.objects.from_today(patient=patient).exists():
            raise ValidationError(
                f"Paciente {patient} já registrado em um relatório para o dia de hoje."
            )

    class Meta:
        model = Report
        fields = "__all__"
