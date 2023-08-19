from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app.report.forms import ReportForm
from app.report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    form = ReportForm

    date_hierarchy = "created_at"

    list_display = [
        "get_shift",
        "get_patient",
        "ventilation_mode",
        "initial_nutritional_route",
        "actual_nutritional_route",
        "treatment",
        "conduct",
        "observation",
    ]

    search_fields = ["patient__name"]
    search_help_test = "Busque pelo nome do paciente"

    list_filter = ["created_at"]

    def get_form(self, request, *args, **kwargs):
        form = super(ReportAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form

    @admin.display(description="relatóio", ordering="-created_at")
    def get_shift(self, obj):
        return str(obj)

    @admin.display(description="paciente", ordering="patient__name")
    def get_patient(self, obj):
        return format_html(
            "{}",
            mark_safe(f"<a href='{obj.patient.get_admin_url()}'>{obj.patient}</a>"),
        )
