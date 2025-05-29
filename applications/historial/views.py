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


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('conserje'), name='dispatch')
class CrearHistorialBathroom(View):
    def post(self, request, alumno_id):
        alumno = get_object_or_404(Alumno, id=alumno_id)
        HistorialBathroom.objects.create(alumno=alumno)
        messages.success(request, f"Registro añadido para {alumno.nombre}.")
        return redirect(request.META.get('HTTP_REFERER', 'listar_alumnos'))