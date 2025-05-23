from django.db import models




# Create your models here.



class Curso(models.Model):
    NIVEL_CHOICES = [
        ('1º ESO', '1º ESO'),
        ('2º ESO', '2º ESO'),
        ('3º ESO', '3º ESO'),
        ('4º ESO', '4º ESO'),
    ]
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)

    def __str__(self):
        return self.nivel

class Grupo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='grupos')
    letra = models.CharField(max_length=1)  # A, B, C...

    class Meta:
        unique_together = ('curso', 'letra')

    def __str__(self):
        return f"{self.curso.nivel} {self.letra}"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='alumnos')

    class Meta:
        unique_together = ('nombre', 'grupo')

    def __str__(self):
        return self.nombre
