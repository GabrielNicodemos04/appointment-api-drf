from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..serializers.professional import ProfessionalSerializer
from ..models import Professional


class ProfessionalViewSet(ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Professional.objects.all()
        
        if hasattr(user, 'professional_profile'):
            return Professional.objects.filter(id=user.professional_profile.id)
        
        return Professional.objects.none()