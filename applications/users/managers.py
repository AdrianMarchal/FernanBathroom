from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):


    #Funcion privada para crear usuarios
    def _create_user(self, email, password, is_staff, is_superuser, type_user_per, **extra_fields):
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            type_user_per=type_user_per,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    #Funcion para crear un usuario
    def create_user(self, email, password,type_user, **extra_fields):
        return self._create_user(email, password, False, False, type_user, **extra_fields)

    #Funcion para crear el super user
    def create_superuser(self, email, password,type_user_per, **extra_fields):
        return self._create_user(email, password,True, True, type_user_per, **extra_fields )