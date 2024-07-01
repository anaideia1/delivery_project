from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from api.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for new user registration
    """
    password = serializers.CharField(
        min_length=8, max_length=100, write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login and receiving jwt tokens
    """
    pass
