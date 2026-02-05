from datetime import timedelta

from ..models.appointment import Appointment

class AppointmentSelector:
    @staticmethod
    def base_queryset():
        return Appointment.objects.all().order_by('appointment_date')
    
    @staticmethod
    def by_customer(qs, customer):
        return qs.filter(customer=customer)
    
    @staticmethod
    def by_professional(qs, professional):
        return qs.filter(professional=professional)
    
    @staticmethod
    def by_status(qs, status):
        return qs.filter(status=status)
    
    @staticmethod
    def conflicts(qs, appointment_date, exclude_id=None):
        qs = qs.filter(
            status=Appointment.STATUS_SCHEDULED,
            appointment_date=appointment_date,
        )

        if exclude_id:
            qs = qs.exclude(id=exclude_id)

        return qs.exists()
    
    @staticmethod
    def by_date(qs, date):
        return qs.filter(appointment_date=date)