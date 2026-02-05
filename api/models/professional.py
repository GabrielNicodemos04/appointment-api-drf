from django.db import models
from django.conf import settings

class Professional(models.Model):
    SPECIALTY_CHOICES = (
        ("THERAPIST", "Therapist"),
        ("COACH", "Coach"),
        ("CONSULTANT", "Consultant"),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='professional_profile',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default="teste@teste.com")
    specialty = models.CharField(
        max_length=20,
        choices=SPECIALTY_CHOICES,
        default="CONSULTANT"
    )
    
    def __str__(self):
        return f"{self.name} - {self.specialty}"