from django.contrib import admin

from applications.alumnos.models import Curso, Grupo, Alumno


# Register your models here.


class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "nivel",
    )

admin.site.register(Curso, CursoAdmin)


class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        "curso",
        "letra"
    )


admin.site.register(Grupo, GrupoAdmin)


class AlumnoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "grupo",
        "necesidad_medica"
    )


admin.site.register(Alumno, AlumnoAdmin)