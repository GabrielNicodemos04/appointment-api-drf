from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.utils.dateparse import parse_date
from django.utils import timezone

from ..serializers.appointment import AppointmentSerializer, AppointmentCancelSerializer
from ..services.appointment_service import AppointmentService   
from ..models import Appointment
from ..permissions import IsCustomerOrAdmin, IsCustomerOrAdminOrProfessionalReadOnly
from ..selectors.appointment_selector import AppointmentSelector

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    ordering_fields = ['appointment_date','created_at','id']
    ordering = ['-appointment_date']
    
    def get_permissions(self):
        if self.action in ["create", "cancel"]:
            return [IsAuthenticated(), IsCustomerOrAdmin()]

        return [IsAuthenticated(), IsCustomerOrAdminOrProfessionalReadOnly()]
    
    def get_queryset(self):
        user = self.request.user
        qs = AppointmentSelector.base_queryset()

        # Admin users can see all appointments
        if user.is_superuser:
            return qs
        
        if hasattr(user, 'customer_profile'):
            qs = AppointmentSelector.by_customer(qs, user.customer_profile)
        elif hasattr(user, 'professional_profile'):
            qs = AppointmentSelector.by_professional(qs, user.professional_profile)
        else:
            return Appointment.objects.none()

        status_param = self.request.query_params.get("status")
        if status_param:
            qs = AppointmentSelector.by_status(qs, status_param)

        date_param = self.request.query_params.get("date")
        today_param = self.request.query_params.get("today")

        if today_param and today_param.lower() == "true":
            today = timezone.now().date()
            qs = AppointmentSelector.by_date(qs, today)
        elif date_param:
            date = parse_date(date_param)
            qs = AppointmentSelector.by_date(qs, date)

        return qs
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        cancel_serializer = AppointmentCancelSerializer(data=request.data)
        cancel_serializer.is_valid(raise_exception=True)

        notes = cancel_serializer.validated_data["notes"]
        AppointmentService.cancel_appointment(appointment=appointment, notes=notes)

        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)