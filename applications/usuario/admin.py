from django.contrib import admin

from applications.usuario.models import Usuario


# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'tipo_usuario', 'is_staff', 'is_active')


admin.site.register(Usuario, UsuarioAdmin)