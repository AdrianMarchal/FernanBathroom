from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
from django.db import models

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField(default=False)
    type_user_per = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type_user_per']
    objects = UserManager()