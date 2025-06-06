from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from applications.alumnos.models import Alumno
from applications.historial.models import HistorialBathroom
from applications.users.decorators import user_type_required
from django.contrib import messages

# Create your views here.


@method_decorator(login_required, name='dispatch')  # Requiere que el usuario haya iniciado sesión
@method_decorator(user_type_required('conserje'), name='dispatch')  # Requiere que el usuario sea "conserje"
class CrearHistorialBathroom(View):

    # Metodo que se ejecuta cuando se hace una solicitud POST
    def post(self, request, alumno_id):
        # Intenta obtener el alumno con el ID proporcionado; si no existe, devuelve error 404
        alumno = get_object_or_404(Alumno, id=alumno_id)

        # Crea un nuevo registro en la base de datos para este alumno en HistorialBathroom
        # Se establece la fecha y hora automáticamente (según el modelo), así como el tramo
        HistorialBathroom.objects.create(alumno=alumno)

        # Muestra un mensaje de éxito al usuario
        messages.success(request, f"Registro añadido para {alumno.nombre}.")

        # Redirige al usuario a la página anterior (o a 'listar_alumnos' si no hay página anterior)
        return redirect(request.META.get('HTTP_REFERER', 'listar_alumnos'))
