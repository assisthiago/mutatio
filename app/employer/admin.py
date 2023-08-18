from django.contrib import admin

from app.employer.forms import EmployerForm
from app.employer.models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    form = EmployerForm
