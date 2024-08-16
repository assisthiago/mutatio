from rest_framework import serializers

from app.patient.models import Diagnosis, Patient, Room


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
