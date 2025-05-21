from django.contrib import admin

from applications.users.models import User


# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'nombre',
        'apellido',
        'is_staff',
        'is_active',
    )

admin.site.register(User, UsersAdmin)