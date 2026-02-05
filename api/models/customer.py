from django.db import models
from django.conf import settings


class Customer(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Ativo"),
        ("INACTIVE", "Inativo"),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='customer_profile',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    plan_status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default="ACTIVE"
    )
    
    def __str__(self):
        return self.name
