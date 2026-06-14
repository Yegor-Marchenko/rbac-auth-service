from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from access.models import Role
from config.constants import MAX_LENGTH


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать email')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=MAX_LENGTH, blank=True)
    token_version = models.PositiveIntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
