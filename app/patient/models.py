from django.db import models


class Diagnosis(models.Model):
    name = models.CharField("diagnóstico", max_length=100)
    description = models.TextField("descrição", max_length=100, default="N/A")
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "diagnosis"
        verbose_name = "diagnóstico"
        verbose_name_plural = "diagnósticos"


class Patient(models.Model):
    name = models.CharField("nome completo", max_length=100)
    age = models.IntegerField("idade")
    room = models.CharField("enfermaria/leito", max_length=10)
    medical_record = models.IntegerField("prontuário")
    hospitalized_in = models.DateField("data da internação")
    sorted_in = models.DateField("data da triagem")
    released = models.BooleanField("alta médica", default=False)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    # Relationships
    diagnosis = models.ForeignKey(
        Diagnosis,
        related_name="patients",
        on_delete=models.CASCADE,
        verbose_name="diagnóstico",
    )

    def __str__(self) -> str:
        return self.name.title()

    class Meta:
        db_table = "patient"
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
