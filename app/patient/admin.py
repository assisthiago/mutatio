from django.contrib import admin

from app.patient.forms import PatientForm
from app.patient.models import Diagnosis, Patient, Room


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["see_more", "ward", "bed", "patient"]

    list_filter = ["ward"]

    readonly_fields = [
        "patient",
    ]

    ordering = ["ward", "bed"]

    search_fields = ["patient__name"]
    search_help_text = "Busque pelo nome e/ou sobrenome do paciente."

    @admin.display(description="#")
    def see_more(self, _):
        return "Ver detalhes"


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm

    list_display = [
        "name",
        "room",
        "age",
        "medical_record",
        "diagnosis",
        "hospitalized_in",
        "sorted_in",
        "eligible",
    ]

    list_editable = ["eligible"]

    list_filter = [
        "diagnosis",
        "hospitalized_in",
        "sorted_in",
        "eligible",
    ]

    ordering = ["name"]

    search_fields = ["name", "medical_record", "room"]
    search_help_text = (
        "Busque pelo nome e/ou sobrenome, prontuário, enfermaria, leito, ou e-mail."
    )
