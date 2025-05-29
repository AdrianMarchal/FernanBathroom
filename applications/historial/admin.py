from django.contrib import admin

from applications.historial.models import HistorialBathroom


# Register your models here.

class HistorialBathroomAdmin(admin.ModelAdmin):
    list_display = (
        "alumno",
        "fecha" ,
        "hora",
        "tramo"
    )

admin.site.register(HistorialBathroom, HistorialBathroomAdmin)