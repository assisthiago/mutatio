from rest_framework import permissions, viewsets

from app.patient.models import Diagnosis, Patient, Room
from app.patient.serializers import (
    DiagnosisSerializer,
    PatientSerializer,
    RoomSerializer,
)


class DiagnosisViewSet(viewsets.ModelViewSet):
    ordering = ["name"]
    queryset = Diagnosis.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiagnosisSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
