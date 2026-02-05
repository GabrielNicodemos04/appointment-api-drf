from rest_framework import serializers
from api.models.appointment import Appointment
from api.services.appointment_service import AppointmentService

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        AppointmentService.validate_business_rules(
            data=attrs,
            instance=self.instance
        )
        return attrs

class AppointmentCancelSerializer(serializers.Serializer):
    notes = serializers.CharField(
        required=True,
        allow_blank=False
    )