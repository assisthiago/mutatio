from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from django_object_actions import DjangoObjectActions, action

from app.report.forms import ReportForm
from app.report.models import Report


@admin.register(Report)
class ReportAdmin(DjangoObjectActions, admin.ModelAdmin):
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

    readonly_fields = ["created_at", "updated_at"]

    search_fields = ["patient__name"]
    search_help_test = "Busque pelo nome do paciente"

    list_filter = ["created_at"]

    @admin.display(description="relatóio", ordering="-created_at")
    def get_shift(self, obj):
        return str(obj)

    @admin.display(description="paciente", ordering="patient__name")
    def get_patient(self, obj):
        return format_html(
            "{}",
            mark_safe(f"<a href='{obj.patient.get_admin_url()}'>{obj.patient}</a>"),
        )

    @action(
        label="Copiar últimos relatórios",
        description="Copia os últimos relatórios disponíveis dos pacientes que não tiverem altas.",
    )
    def copy_previous_reports(self, request, obj):
        if reports := Report.objects.from_today():
            self._messages(
                request,
                "Existe %d relatório cadastrado para o dia de hoje.",
                "Existem %d relatórios cadastrados para o dia de hoje.",
                len(reports),
                messages.WARNING,
            )

        if last_reports_availables := Report.objects.last_availables(
            patient__released=False
        ):
            reports_to_copy = []
            for report in last_reports_availables:
                report.pk = None
                reports_to_copy.append(report)

            updated = Report.objects.bulk_create(reports_to_copy)
            self._messages(
                request,
                "%d relatório copiado com sucesso.",
                "%d relatórios copiados com sucesso.",
                len(updated),
                messages.SUCCESS,
            )

        return self.message_user(
            request,
            "Nenhum relatório foi encontrado.",
            messages.WARNING,
        )

    changelist_actions = [
        "copy_previous_reports",
    ]

    def _messages(self, request, singular_msg, plural_msg, length, level):
        return self.message_user(
            request,
            ngettext(
                singular_msg,
                plural_msg,
                length,
            )
            % length,
            level,
        )
