from django.apps import AppConfig


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.patient"
    verbose_name = "Informações gerais de pacientes"
