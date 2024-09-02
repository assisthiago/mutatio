from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters, permissions, response, viewsets

from app.patient.models import Diagnosis, Patient, Room
from app.patient.serializers import (
    DiagnosisSerializer,
    PatientCreateUpdateSerializer,
    PatientSerializer,
    RoomSerializer,
)


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiagnosisSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering = ["name"]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "medical_record"]
    ordering = ["name", "age"]

    def create(self, request, *args, **kwargs):
        serializer = PatientCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = get_object_or_404(Room, pk=serializer.validated_data["room"])
        diagnoses = get_list_or_404(
            Diagnosis, pk__in=serializer.validated_data["diagnoses"]
        )

        patient = Patient.objects.create(
            name=serializer.validated_data["name"],
            age=serializer.validated_data["age"],
            medical_record=serializer.validated_data["medical_record"],
            hospitalized_in=serializer.validated_data["hospitalized_in"],
            sorted_in=serializer.validated_data["sorted_in"],
            nutritional_route=serializer.validated_data["nutritional_route"],
            eligible=serializer.validated_data["eligible"],
            room=room,
        )

        patient.diagnoses.set(diagnoses)
        patient.save()

        return response.Response(status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PatientCreateUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        room = get_object_or_404(Room, pk=serializer.validated_data["room"])
        diagnoses = get_list_or_404(
            Diagnosis, pk__in=serializer.validated_data["diagnoses"]
        )

        instance.name = serializer.validated_data["name"]
        instance.age = serializer.validated_data["age"]
        instance.medical_record = serializer.validated_data["medical_record"]
        instance.hospitalized_in = serializer.validated_data["hospitalized_in"]
        instance.sorted_in = serializer.validated_data["sorted_in"]
        instance.nutritional_route = serializer.validated_data["nutritional_route"]
        instance.eligible = serializer.validated_data["eligible"]
        instance.room = room

        instance.diagnoses.set(diagnoses)
        instance.save()

        return response.Response(status=200)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["ward"]
    ordering = ["ward", "bed"]
