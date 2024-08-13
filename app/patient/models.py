from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Diagnosis(models.Model):
    name = models.CharField("diagnóstico", max_length=100)
    description = models.TextField("descrição", max_length=100, default="N/A")
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "diagnosis"
        ordering = ("name",)
        verbose_name = "diagnóstico"
        verbose_name_plural = "diagnósticos"


class Room(models.Model):
    ward = models.CharField("enfermaria", max_length=10)
    bed = models.PositiveSmallIntegerField("leito")
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.ward}{self.bed}"

    class Meta:
        db_table = "room"
        constraints = [
            models.UniqueConstraint(
                fields=["ward", "bed"],
                name="unique_room",
            )
        ]
        verbose_name = "quarto"
        verbose_name_plural = "quartos"


class Patient(models.Model):
    name = models.CharField("nome completo", max_length=100)
    age = models.IntegerField("idade")
    medical_record = models.IntegerField("prontuário")
    hospitalized_in = models.DateField("data da internação")
    sorted_in = models.DateField("data da triagem")
    nutritional_route = models.CharField("via nutricional", max_length=100)
    eligible = models.BooleanField("elegível", default=False)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)
    history = AuditlogHistoryField()

    # Relationships
    diagnoses = models.ManyToManyField(
        Diagnosis,
        related_name="patients",
        verbose_name="diagnósticos",
    )

    room = models.OneToOneField(
        Room, related_name="patient", on_delete=models.CASCADE, verbose_name="quarto"
    )

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    def __str__(self) -> str:
        return self.name.title()

    class Meta:
        db_table = "patient"
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"


# Automatically logging changes.
auditlog.register(Diagnosis)
auditlog.register(Room)
auditlog.register(Patient)
