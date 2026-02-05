from django.db import models
from django.conf import settings
from .customer import Customer
from .professional import Professional

class Appointment(models.Model):
    STATUS_CANCELLED = "CANCELLED"
    STATUS_SCHEDULED = "SCHEDULED"

    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )

    professional = models.ForeignKey(
        Professional, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Appointment on {self.appointment_date} between {self.customer.name} and {self.professional.name}"