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
        "see_more",
        "created_at",
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

    @admin.display(description="#")
    def see_more(self, _):
        return "Ver detalhes"

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
            return self._messages(
                request=request,
                singular_msg="Existe %d relatório cadastrado para o dia de hoje.",
                plural_msg="Existem %d relatórios cadastrados para o dia de hoje.",
                length=len(reports),
                level=messages.WARNING,
            )

        if last_reports_availables := Report.objects.last_availables(
            patient__eligible=True
        ):
            reports_to_copy = []
            for report in last_reports_availables:
                report.pk = None
                reports_to_copy.append(report)

            updated = Report.objects.bulk_create(reports_to_copy)
            return self._messages(
                request=request,
                singular_msg="%d relatório copiado com sucesso.",
                plural_msg="%d relatórios copiados com sucesso.",
                length=len(updated),
                level=messages.SUCCESS,
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
