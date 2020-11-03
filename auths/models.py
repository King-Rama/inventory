from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_pos = models.BooleanField(default=False, blank=True, null=True)
    is_manager = models.BooleanField(default=False, blank=True, null=True)
    is_super_manager = models.BooleanField(default=False, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

