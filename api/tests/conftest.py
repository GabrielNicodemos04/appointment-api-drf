import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from api.models.customer import Customer
from api.models.professional import Professional
from api.models.appointment import Appointment

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="123456"
    )

@pytest.fixture
def customer(user):
    return Customer.objects.create(
        user=user,
        name="Test Customer",
        email="customer@test.com"
    )

@pytest.fixture
def professional():
    prof_user = User.objects.create_user(
        username="profuser",
        password="123456"
    )
    return Professional.objects.create(
        user=prof_user,
        name="Test Professional",
        email="professional@test.com"
    )

@pytest.fixture
def appointment(customer, professional):
    future_date = timezone.now() + timedelta(days=1)
    future_date = future_date.replace(minute=0, second=0, microsecond=0)
    return Appointment.objects.create(
        customer=customer,
        professional=professional,
        appointment_date=future_date
    )

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, customer):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(customer.user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def professional_authenticated_client(api_client, professional):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(professional.user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client