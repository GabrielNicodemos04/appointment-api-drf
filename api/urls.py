from .views.appointment import AppointmentViewSet
from .views.customer import CustomerViewSet
from .views.professional import ProfessionalViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'professionals', ProfessionalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]