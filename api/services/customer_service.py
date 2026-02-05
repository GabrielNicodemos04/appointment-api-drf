from rest_framework.exceptions import ValidationError
from api.models.customer import Customer

class CustomerService:
    @staticmethod
    def validate_business_rules(data, instance=None):
        email = data.get("email")

        if email:
            qs = Customer.objects.filter(email=email)

            if instance:
                qs = qs.exclude(id=instance.id)

            if qs.exists():
                raise ValidationError({
                    "email": "Já existe um cliente ativo com este email."
                })
