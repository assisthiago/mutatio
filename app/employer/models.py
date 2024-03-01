from django.contrib.auth.models import User
from django.db import models


class Employer(models.Model):
    user = models.OneToOneField(
        User, related_name="employer", on_delete=models.CASCADE, verbose_name="usuário"
    )
    phone = models.CharField("telefone", max_length=11)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}".title()

    class Meta:
        db_table = "employer"
        verbose_name = "empregado"
        verbose_name_plural = "empregados"
