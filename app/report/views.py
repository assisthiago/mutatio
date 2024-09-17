from django.utils.translation import ngettext
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.report.models import Report
from app.report.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="copy", url_name="copy")
    def copy_previous_reports(self, request):
        if reports := Report.objects.from_today():
            return Response(
                data={
                    "detail": ngettext(
                        "Existe %d relatório criado para o dia de hoje.",
                        "Existem %d relatórios criados para o dia de hoje.",
                        len(reports),
                    )
                    % len(reports)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if last_reports_availables := Report.objects.last_availables(
            patient__eligible=True
        ):
            reports_to_copy = []
            for report in last_reports_availables:
                report.pk = None
                reports_to_copy.append(report)

            updated = Report.objects.bulk_create(reports_to_copy)

            return Response(
                data={
                    "detail": ngettext(
                        "%d relatório copiado com sucesso.",
                        "%d relatórios copiados com sucesso.",
                        len(updated),
                    )
                    % len(updated)
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data={"detail": "Nenhum relatório foi encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )
