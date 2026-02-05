# api/tests/test_views.py
import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from api.models.appointment import Appointment

@pytest.mark.django_db
class TestAppointmentViewSet:
    def test_create_valid_appointment(self, authenticated_client, customer, professional):
        """Teste de criação de agendamento válido"""
        future_date = timezone.now() + timedelta(days=1)
        future_date = future_date.replace(minute=0, second=0, microsecond=0)  # Intervalo de 30 min

        data = {
            "customer": customer.id,
            "professional": professional.id,
            "appointment_date": future_date.isoformat(),
            "notes": "Consulta inicial"
        }

        url = reverse('appointment-list')
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Appointment.objects.count() == 1
        appointment = Appointment.objects.first()
        assert appointment.customer == customer
        assert appointment.professional == professional

    def test_create_appointment_conflict(self, authenticated_client, customer, professional, appointment):
        """Teste de conflito de horário"""
        # Tenta criar outro agendamento no mesmo horário
        data = {
            "customer": customer.id,
            "professional": professional.id,
            "appointment_date": appointment.appointment_date.isoformat(),
            "notes": "Outro agendamento"
        }

        url = reverse('appointment-list')
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Já existe um agendamento" in str(response.data)

    def test_create_appointment_past_date(self, authenticated_client, customer, professional):
        """Teste de agendamento em data passada"""
        past_date = timezone.now() - timedelta(hours=1)

        data = {
            "customer": customer.id,
            "professional": professional.id,
            "appointment_date": past_date.isoformat(),
            "notes": "Agendamento passado"
        }

        url = reverse('appointment-list')
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "datas passadas" in str(response.data)

    def test_permission_customer_access_own_data(self, authenticated_client, customer, professional, appointment):
        """Teste de permissão (usuário acessando seus próprios dados)"""
        url = reverse('appointment-detail', kwargs={'pk': appointment.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['customer'] == customer.id

    def test_permission_customer_cannot_access_other_customer_data(self, api_client, customer, professional):
        """Teste de permissão (usuário acessando outro usuário)"""
        # Criar outro customer
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(username="other", password="123")
        other_customer = customer.__class__.objects.create(
            user=other_user,
            name="Other Customer",
            email="other@test.com"
        )
        other_appointment = Appointment.objects.create(
            customer=other_customer,
            professional=professional,
            appointment_date=timezone.now() + timedelta(days=2)
        )

        # Autenticar como customer original
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(customer.user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse('appointment-detail', kwargs={'pk': other_appointment.pk})
        response = api_client.get(url)

        # Deve retornar 404 ou vazio, pois não tem permissão
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]

    def test_permission_professional_read_only(self, professional_authenticated_client, customer, professional, appointment):
        """Teste de permissão (profissional acessando dados indevidos)"""
        # Profissional pode ler
        url = reverse('appointment-detail', kwargs={'pk': appointment.pk})
        response = professional_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Mas não pode criar
        future_date = timezone.now() + timedelta(days=3)
        future_date = future_date.replace(minute=0, second=0, microsecond=0)
        data = {
            "customer": customer.id,
            "professional": professional.id,
            "appointment_date": future_date.isoformat(),
            "notes": "Tentativa de criação"
        }
        url = reverse('appointment-list')
        response = professional_authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_jwt_authentication_required(self, api_client, customer, professional):
        """Teste de autenticação JWT"""
        future_date = timezone.now() + timedelta(days=1)
        future_date = future_date.replace(minute=0, second=0, microsecond=0)

        data = {
            "customer": customer.id,
            "professional": professional.id,
            "appointment_date": future_date.isoformat(),
            "notes": "Sem autenticação"
        }

        url = reverse('appointment-list')
        response = api_client.post(url, data, format='json')

        # Deve falhar sem autenticação
        assert response.status_code == status.HTTP_401_UNAUTHORIZED