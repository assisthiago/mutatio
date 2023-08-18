from django import forms

from app.report.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
