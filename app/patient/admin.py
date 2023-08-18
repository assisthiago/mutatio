from django.contrib import admin

from app.patient.forms import PatientForm
from app.patient.models import Diagnosis, Patient


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm

    list_display = [
        "name",
        "age",
        "room",
        "medical_record",
        "diagnosis",
        "hospitalized_in",
        "sorted_in",
        "released",
    ]

    list_editable = ["released"]

    list_filter = [
        "diagnosis",
        "hospitalized_in",
        "sorted_in",
        "released",
    ]

    ordering = ["name"]

    search_fields = ["name", "medical_record", "room"]
    search_help_text = (
        "Busque pelo nome e/ou sobrenome, prontuário, enfermaria, leito, ou e-mail."
    )
