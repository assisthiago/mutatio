from django.db import models

from app.employer.models import Employer
from app.patient.models import Patient


class Report(models.Model):
    ventilation_mode = models.CharField("modo ventilatório", max_length=100)
    initial_nutritional_route = models.CharField(
        "via nutricional inicial", max_length=100
    )
    actual_nutritional_route = models.CharField("via nutricional atual", max_length=100)
    treatment = models.CharField("atendimento", max_length=100)
    conduct = models.CharField("conduta", max_length=100)
    observation = models.TextField("observação", max_length=100, default="N/A")
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    # Relationships
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="paciente",
    )

    def __str__(self) -> str:
        return f"Relatório {self.created_at.strftime('%Y%m%d')}"

    class Meta:
        db_table = "report"
        verbose_name = "relatório"
        verbose_name_plural = "relatórios"
