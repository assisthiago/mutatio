from django.contrib import admin

from app.report.forms import ReportForm
from app.report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    form = ReportForm

    def get_form(self, request, *args, **kwargs):
        form = super(ReportAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form
