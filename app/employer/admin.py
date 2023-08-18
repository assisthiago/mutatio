from django.contrib import admin

from app.employer.forms import EmployerForm
from app.employer.models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    form = EmployerForm

    list_display = ["get_name", "phone", "get_email"]

    ordering = ["user__first_name"]

    search_fields = ["user__first_name", "user__last_name", "user__email"]
    search_help_text = "Busque pelo nome, sobrenome ou e-mail."

    @admin.display(ordering="user__first_name", description="nome")
    def get_name(self, obj):
        return str(obj)

    @admin.display(description="e-mail")
    def get_email(self, obj):
        return obj.user.email
