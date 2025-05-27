from django.shortcuts import render

# Create your views here.

# views.py
import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Grupo, Alumno, Curso


import csv
import io

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Grupo, Alumno, Curso
import csv
import io

from ..users.decorators import user_type_required


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class ImportarCSVView(View):
    def get(self, request):
        return render(request, 'alumnos/importar.html')

    def post(self, request):
        alumnos_rechazados = []
        alumnos_duplicados = []

        archivo = request.FILES.get('archivo')
        if not archivo.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser un CSV.')
            return redirect('importar_csv')

        try:
            contenido = archivo.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            archivo.seek(0)
            contenido = archivo.read().decode('latin1')

        io_string = io.StringIO(contenido)
        lector = csv.DictReader(io_string)

        for fila in lector:
            if 'Alumno/a' not in fila or 'Unidad' not in fila:
                messages.error(request, f"Columnas no válidas: {fila.keys()}")
                return redirect('importar_csv')

            nombre = fila['Alumno/a'].strip()
            unidad = fila['Unidad'].strip()

            if unidad == '':
                alumnos_rechazados.append(nombre)
                continue

            try:
                curso_str, letra = unidad.split('º ESO ')
                curso_str = f"{curso_str}º ESO"
            except ValueError:
                alumnos_rechazados.append(nombre)
                continue

            curso, _ = Curso.objects.get_or_create(nivel=curso_str)
            grupo, _ = Grupo.objects.get_or_create(curso=curso, letra=letra)

            if Alumno.objects.filter(nombre=nombre, grupo=grupo).exists():
                alumnos_duplicados.append(nombre)
                continue

            Alumno.objects.create(nombre=nombre, grupo=grupo)

        messages.success(request, 'Alumnos importados correctamente.')
        return render(request, 'alumnos/importar.html', {
            'alumnos_rechazados': alumnos_rechazados,
            'alumnos_duplicados': alumnos_duplicados
        })



@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class BorrarDatosView(View):
    def get(self, request):
        return render(request, 'alumnos/borrar_confirmacion.html')

    def post(self, request):
        Alumno.objects.all().delete()
        Grupo.objects.all().delete()
        Curso.objects.all().delete()
        messages.success(request, 'Todos los datos han sido eliminados correctamente.')
        return redirect('importar_csv')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador', 'profesor', 'conserje'), name='dispatch')
class ListarAlumnos(ListView):
    # Se puede sobrescribir el template name asi
    # path('usuarios/', ListarUsuarios.as_view(template_name='usuarios/lista_general.html'), name='usuarios_lista_general'),
    model = Alumno
    template_name = "alumnos/listar_alumnos.html"
    context_object_name = 'alumnos'
    paginate_by = 25

    def get_queryset(self):
        return Alumno.objects.select_related('grupo__curso').order_by(
            'grupo__curso__nivel', 'grupo__letra', 'nombre'
        )