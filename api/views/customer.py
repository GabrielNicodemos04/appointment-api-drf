from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..serializers.customer import CustomerSerializer
from ..models import Customer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or hasattr(user, 'professional_profile'):
            return Customer.objects.all()
        
        if hasattr(user, 'customer_profile'):
            return Customer.objects.filter(id=user.customer_profile.id)
        
        return Customer.objects.none()