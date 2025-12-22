from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.conf import settings


class CostumeUser(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    MASTER = 'master'
    SLAVE = 'slave'
    SUPERUSER = 'superuser'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MASTER, 'Master'),
        (SLAVE, 'Slave'),
        (SUPERUSER, 'Superuser'),
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=285, null=False)
    last_name = models.CharField(max_length=258, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Slave')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_master = models.BooleanField(default=False)
    is_slave = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    objects = CustomUserManager()

    def __str__(self):
        return  f'this table belong to this user : {self.first_name}  {self.last_name} '




class TwoFactorCode(models.Model):
    user = models.ForeignKey(CostumeUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user



class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    device = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} | {self.ip_address} | {self.device}"

