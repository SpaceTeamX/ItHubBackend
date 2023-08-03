from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from .services import get_path_upload_user_avatar, validate_size_image


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
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
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    data_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    GENDERS = [
        ('he', "Man"),
        ("she", "Woman"),
        ("none", "Anonymous"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_path_upload_user_avatar,
                               validators=[validate_size_image],
                               default="default/avatar.png")

    gender = models.CharField(max_length=4, choices=GENDERS, default="none")

    def __str__(self):
        return self.user.username

