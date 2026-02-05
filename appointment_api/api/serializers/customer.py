from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.customer import Customer
from api.services.customer_service import CustomerService

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['name'],
            is_staff=False,
        )

        validated_data.pop('user', None)
        
        customer = Customer.objects.create(
            user=user,
            **validated_data
        )

        return customer

    def validate(self, attrs):
        CustomerService.validate_business_rules(
            data=attrs,
            instance=self.instance
        )

        return attrs