from os import remove
from shutil import rmtree

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from ithub.settings import MEDIA_ROOT
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_writable_nested import WritableNestedModelSerializer

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "password"]
        read_only_fields = (
            'id', "data_joined", "is_active", "is_superuser",
            "groups", "user_permissions"
        )


class AnotherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "password", "email"]


class MeProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        if "avatar" in validated_data.keys():
            if instance.avatar.url != "/media/default/avatar.png":
                try:
                    remove(instance.avatar.path)
                except Exception as ex:
                    print(ex)

        return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = '__all__'


class AnotherProfileSerializer(serializers.ModelSerializer):
    user = AnotherUserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            if user.is_active:
                return user

            raise ValidationError('Your account is not active')
        raise ValidationError('Incorrect Credentials Passed.')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        validate_password(attrs['password'])
        return super().validate(attrs)

    def create(self, validated_data: dict):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data["email"],
            validated_data['password']
        )

        return user





class DeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=150)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        instance = self.instance

        if not instance.email == email:
            raise ValidationError("email incorrectly")
        if not instance.check_password(password):
            raise ValidationError("password incorrectly")

        try:
            rmtree(MEDIA_ROOT / "users" / str(instance.id))
        except Exception as ex:
            print(ex)

        instance.delete()

        return {"success": True}


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    new_password_repeat = serializers.CharField(max_length=200)

    def validate(self, attrs):
        password = attrs.get("password")
        instance = self.instance

        if not instance.check_password(password):
            raise ValidationError("The current password is incorrect")

        new_password = attrs.get("new_password")
        new_password_repeat = attrs.get("new_password_repeat")

        if new_password != new_password_repeat or instance.check_password(new_password):
            raise ValidationError("The new password does not match the recurrence, or the new password is the same as "
                                  "the old one")

        validate_password(new_password, self.instance)

        instance.set_password(new_password)
        instance.save()

        return {"success": True}
