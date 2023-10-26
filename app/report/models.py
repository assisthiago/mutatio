from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from app.patient.models import Patient
from app.report.managers import ReportManager


class Report(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="paciente",
    )
    ventilation_mode = models.CharField("modo ventilatório", max_length=100)
    initial_nutritional_route = models.CharField(
        "via nutricional inicial", max_length=100
    )
    actual_nutritional_route = models.CharField("via nutricional atual", max_length=100)
    treatment = models.CharField("atendimento", max_length=100)
    conduct = models.TextField("conduta", max_length=100)
    observation = models.TextField("observação", max_length=255, default="N/A")
    created_at = models.DateField("criado em", auto_now_add=True)
    updated_at = models.DateField("atualizado em", auto_now=True)

    history = AuditlogHistoryField()

    objects = ReportManager.as_manager()

    def __str__(self) -> str:
        return self.created_at.strftime("%Y%m%d")

    class Meta:
        db_table = "report"
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "created_at"],
                name="unique_patient_per_day",
            )
        ]
        verbose_name = "relatório"
        verbose_name_plural = "relatórios"


auditlog.register(Report)
