from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.professional import Professional

User = get_user_model()

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['name'],
            is_staff=False,
        )

        validated_data.pop('user', None)
        
        professional = Professional.objects.create(
            user=user,
            **validated_data
        )

        return professional