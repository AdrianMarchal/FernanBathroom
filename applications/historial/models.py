from django.utils import timezone

from django.db import models

from applications.alumnos.models import Alumno


# Create your models here.

class HistorialBathroom(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    hora = models.TimeField(default=timezone.now)
    tramo = models.PositiveSmallIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if self.hora >= timezone.datetime.strptime('08:00', '%H:%M').time() and self.hora <= timezone.datetime.strptime('11:00', '%H:%M').time():
            self.tramo = 1
        elif self.hora > timezone.datetime.strptime('11:00', '%H:%M').time() and self.hora <= timezone.datetime.strptime('14:00', '%H:%M').time():
            self.tramo = 2
        else:
            self.tramo = -1  # fuera de tramo, o puedes usar None con un campo nullable
        super().save(*args, **kwargs)