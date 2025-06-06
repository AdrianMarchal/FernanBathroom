import pytz

from django.db import models
from datetime import time
from applications.alumnos.models import Alumno


# Create your models here.
from django.utils.timezone import now
from django.utils import timezone


# Función para obtener la hora actual en la zona horaria de Madrid
def current_time_madrid():
    madrid_tz = pytz.timezone('Europe/Madrid')  # Define la zona horaria de Madrid
    now_madrid = timezone.now().astimezone(madrid_tz)  # Convierte la hora actual a esa zona horaria
    return now_madrid.time()  # Retorna solo la hora (sin la fecha)



# Modelo para registrar el historial de visitas al baño
class HistorialBathroom(models.Model):
    # Relación con un alumno. Si el alumno se elimina, también se eliminarán sus registros.
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    # Fecha del registro. Por defecto, se usa la fecha actual.
    fecha = models.DateField(default=now)

    # Hora del registro. Por defecto, se usa la hora actual en Madrid.
    hora = models.TimeField(default=current_time_madrid)

    # Campo que indica el tramo horario en el que ocurrió la salida.
    # No editable directamente (se asigna automáticamente al guardar).
    tramo = models.PositiveSmallIntegerField(editable=False)

    # Metodo que se ejecuta al guardar una instancia del modelo
    def save(self, *args, **kwargs):

        # Determina a qué tramo pertenece la hora registrada
        if time(8, 0) <= self.hora <= time(11, 0):
            self.tramo = 1  # Tramo 1: entre las 08:00 y las 11:00
        elif time(11, 0) < self.hora <= time(15, 0):
            self.tramo = 2  # Tramo 2: entre las 11:01 y las 15:00
        else:
            self.tramo = 0  # Fuera del horario considerado válido

        # Llama al metodo `save` original de Django para guardar el objeto
        super().save(*args, **kwargs)
