import bcrypt
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from access.models import Role
from config.constants import MAX_LENGTH


class CustomUserManager(models.Manager):

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

    def create_admin(self, email, password):
        role, created = Role.objects.get_or_create(
            title="admin"
        )
        return self.create_user(
            email=email,
            password=password,
            role=role
        )

    def normalize_email(self, email):
        email_parts = email.strip().rsplit('@', 1)
        domain = email_parts[-1].lower()
        return email_parts[0] + '@' + domain


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)
    middle_name = models.CharField(max_length=MAX_LENGTH, blank=True)
    password = models.CharField(max_length=MAX_LENGTH)
    token_version = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def set_password(self, password):
        password_bytes = password.encode(encoding="utf-8")
        self.password = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt()
        ).decode(encoding="utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
