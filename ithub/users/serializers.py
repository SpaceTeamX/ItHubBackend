from django.contrib.auth import authenticate

from .models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            if user.is_active:
                return user

            raise serializers.ValidationError('Your account is not active')
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data: dict):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data["email"],
            validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', "avatar",
            "age", "country", "city", "avatar", "data_joined",
            "last_name", "first_name"
        )
