from django.db import models

from django.contrib.auth.models import BaseUserManager


# Clase personalizada para gestionar la creación de usuarios y superusuarios
class UserManager(BaseUserManager, models.Manager):

    # Función privada que maneja la lógica común de creación de usuarios (tanto normales como superusuarios)
    def _create_user(self, email, password, is_staff, is_superuser, type_user_per, **extra_fields):
        # Crea una instancia del modelo de usuario con los campos obligatorios y extras
        user = self.model(
            email=email,
            is_staff=is_staff,  # Define si el usuario tiene acceso al admin
            is_superuser=is_superuser,  # Define si es superusuario
            type_user_per=type_user_per,
            # Campo personalizado para el tipo de usuario (ej. 'profesor', 'conserje', etc.)
            **extra_fields  # Otros campos opcionales (nombre, apellido, etc.)
        )

        # Hashea y asigna la contraseña
        user.set_password(password)

        # Guarda el usuario en la base de datos (usando la conexión por defecto)
        user.save(using=self._db)
        return user

    #Funcion para crear un usuario
    def create_user(self, email, password,type_user, **extra_fields):
        return self._create_user(email, password, False, False, type_user, **extra_fields)

    #Funcion para crear el super user
    def create_superuser(self, email, password,type_user_per, **extra_fields):
        return self._create_user(email, password,True, True, type_user_per, **extra_fields )