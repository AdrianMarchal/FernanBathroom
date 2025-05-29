import pytz
from django.utils import timezone

from django.db import models
from datetime import time
from django.utils.timezone import now
from applications.alumnos.models import Alumno


# Create your models here.

from django.utils.timezone import now
from django.utils import timezone


def current_time_madrid():
    madrid_tz = pytz.timezone('Europe/Madrid')
    now_madrid = timezone.now().astimezone(madrid_tz)
    return now_madrid.time()


class HistorialBathroom(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateField(default=now)
    hora = models.TimeField(default=current_time_madrid)
    tramo = models.PositiveSmallIntegerField(editable=False)

    def save(self, *args, **kwargs):
        print("Hora guardada:", self.hora)
        if time(8, 0) <= self.hora <= time(11, 0):
            self.tramo = 1
        elif time(11, 0) < self.hora <= time(15, 0):
            self.tramo = 2
        else:
            self.tramo = 0  # fuera del horario útil

        super().save(*args, **kwargs)
