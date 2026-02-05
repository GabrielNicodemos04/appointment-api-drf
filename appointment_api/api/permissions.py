from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
        Admin tem acesso total.
        Outros usuários apenas leitura (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False
    
class IsCustomerOrAdmin(BasePermission):
    """
        Customer só acessa seus próprios agendamentos.
        Admin acessa tudo.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'customer_profile'):
            return True
        return False
    
class IsCustomerOrAdminOrProfessionalReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return (
                hasattr(request.user, "customer_profile") or
                hasattr(request.user, "professional_profile")
            )

        return hasattr(request.user, "customer_profile")