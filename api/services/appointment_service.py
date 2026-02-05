from rest_framework.exceptions import ValidationError
from api.models.appointment import Appointment
from django.utils import timezone
from datetime import timedelta
from ..selectors.appointment_selector import AppointmentSelector

class AppointmentService:
    INTERVAL_MINUTES = 30

    @staticmethod
    def validate_business_rules(data, instance=None):
        appointment_date = data.get("appointment_date")

        if not appointment_date:
            return

        AppointmentService._validate_not_past_date(appointment_date)
        AppointmentService._validate_fixed_interval(appointment_date)

        professional = (
            data.get("professional")
            or getattr(instance, "professional", None)
        )

        AppointmentService._validate_conflict(
            professional,
            appointment_date,
            instance
        )
    
    @staticmethod
    def _validate_not_past_date(appointment_date):
        now = timezone.now()

        if appointment_date < now:
            raise ValidationError({
                "appointment_date": "Não é permitido criar agendamentos para datas passadas."
            })
    
    @staticmethod
    def _validate_fixed_interval(appointment_date):
        minute = appointment_date.minute
        seconds = appointment_date.second
        microseconds = appointment_date.microsecond
        if minute % AppointmentService.INTERVAL_MINUTES != 0 or seconds != 0 or microseconds != 0:
            raise ValidationError({
                "appointment_date": f"Os agendamentos devem ser feitos em intervalos de {AppointmentService.INTERVAL_MINUTES} minutos."
            })
        
    @staticmethod
    def _validate_conflict(
        professional,
        appointment_date,
        instance=None
    ):
        if not professional:
            return

        qs = Appointment.objects.filter(professional=professional)

        conflict = AppointmentSelector.conflicts(
            qs,
            appointment_date=appointment_date,
            exclude_id=instance.id if instance else None
        )

        if conflict:
            raise ValidationError(
                "Já existe um agendamento para este profissional neste horário."
            )
    
    @staticmethod
    def validate_cancel(appointment: Appointment):
        now = timezone.now()

        if appointment.status == appointment.STATUS_CANCELLED:
            raise ValidationError("Este agendamento já foi cancelado.")

        if appointment.appointment_date <= now:
            raise ValidationError(
                "Não é possível cancelar um agendamento após o horário marcado."
            )
        
    def cancel_appointment(appointment: Appointment, notes: str = "") -> Appointment:
        AppointmentService.validate_cancel(appointment)
        appointment.status = appointment.STATUS_CANCELLED
        appointment.notes = f"\nAgendamento cancelado. Motivo: {notes or 'Nenhum motivo informado.'}"
        appointment.save()

        return appointment