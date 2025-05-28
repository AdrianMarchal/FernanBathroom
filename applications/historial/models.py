from django.utils import timezone

from django.db import models

from applications.alumnos.models import Alumno


# Create your models here.

class HistorialBathroom(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)  # <-- NUEVO CAMPO
    hora = models.TimeField(default=timezone.now)
    tramo = models.PositiveSmallIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if self.hora >= timezone.datetime.strptime('08:00', '%H:%M').time() and self.hora <= timezone.datetime.strptime('11:00', '%H:%M').time():
            self.tramo = 1
        elif self.hora > timezone.datetime.strptime('11:00', '%H:%M').time() and self.hora <= timezone.datetime.strptime('15:00', '%H:%M').time():
            self.tramo = 2
        else:
            self.tramo = -1
        super().save(*args, **kwargs)