from rest_framework import serializers

from app.patient.models import Diagnosis, Patient, Room


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    room_str = serializers.StringRelatedField(source="room", read_only=True)
    diagnoses = DiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"


class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    room = serializers.IntegerField()
    diagnoses = serializers.ListField(
        child=serializers.IntegerField(min_value=0), allow_empty=False
    )

    class Meta:
        model = Patient
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
