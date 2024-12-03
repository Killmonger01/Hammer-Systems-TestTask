import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def generate_invite_code(self):
        """Генерация случайного 6-значного инвайт-кода"""
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            self.save()

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

class InviteRelation(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_users')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter')
    created_at = models.DateTimeField(auto_now_add=True)
