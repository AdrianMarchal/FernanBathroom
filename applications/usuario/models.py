from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, tipo_usuario, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        usuario = self.model(
            email=email,
            nombre=nombre,
            tipo_usuario=tipo_usuario,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, password=None, tipo_usuario='administrador', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if tipo_usuario != 'administrador':
            raise ValueError("El superusuario debe tener tipo_usuario='administrador'")

        return self.create_user(
            email=email,
            nombre=nombre,
            tipo_usuario=tipo_usuario,
            password=password,
            **extra_fields
        )


class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPOS_USUARIO = (
        ('administrador', 'Administrador'),
        ('profesor', 'Profesor'),
    )

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'tipo_usuario']

    def __str__(self):
        return f"{self.nombre} ({self.tipo_usuario})"
