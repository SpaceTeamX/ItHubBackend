from os import remove
from shutil import rmtree

from django.contrib.auth import authenticate
from ithub.settings import MEDIA_ROOT
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


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


class MeUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        if "avatar" in validated_data.keys():
            print(instance.avatar.url)
            if instance.avatar.url != "/media/default/avatar.png":
                try:
                    remove(instance.avatar.path)
                except Exception as ex:
                    print(ex)

        new_inst = super(MeUserSerializer, self).update(instance, validated_data)
        return new_inst

    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "password"]


class AnotherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["email", "groups", "user_permissions", "last_login", "password"]


class DeleteUserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        instance = self.instance

        if not instance.email == email:
            raise ValidationError("email incorrectly")
        if not instance.check_password(password):
            raise ValidationError("password incorrectly")

        rmtree(MEDIA_ROOT / "users" / str(instance.id))
        instance.delete()

        return {"success": "true"}

    class Meta:
        model = User
        fields = ["email", "password"]


class PasswordResetSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=200)
    new_password_repeat = serializers.CharField(max_length=200)

    def validate(self, attrs):
        password = attrs.get("password")
        instance = self.instance

        if not instance.check_password(password):
            raise ValidationError("password incorrectly")

        new_password = attrs.get("new_password")
        new_password_repeat = attrs.get("new_password_repeat")

        if new_password != new_password_repeat or instance.check_password(new_password):
            raise ValidationError("New password incorrectly")

        instance.set_password(new_password)
        instance.save()

        return {"success": "true"}

    class Meta:
        model = User
        fields = ["password", "new_password", "new_password_repeat"]
