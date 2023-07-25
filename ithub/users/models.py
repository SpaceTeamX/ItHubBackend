from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from .services import get_path_upload_user_avatar, validate_size_image


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have email address")
        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDERS = [
        ('he', "Man"),
        ("she", "Woman"),
        ("none", "Anonymous"),
    ]

    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    age = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_path_upload_user_avatar,
                               validators=[validate_size_image],
                               blank=True,
                               default="default/avatar.png")

    data_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=4, choices=GENDERS, default="none")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()


