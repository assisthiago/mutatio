from rest_framework import serializers

from app.report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    patient__str = serializers.CharField(source="patient", read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
