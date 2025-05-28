from django.shortcuts import render

# Create your views here.

# views.py
import csv
import io

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Grupo, Alumno, Curso


from ..users.decorators import user_type_required


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class ImportarCSVView(View):
    def get(self, request):
        return render(request, 'alumnos/importar.html')

    def post(self, request):
        alumnos_rechazados = []   # Lista de alumnos sin curso válido o con errores
        alumnos_duplicados = []   # Alumnos ya asignados al mismo grupo (no se reimportan)
        alumnos_cambiados = []    # Alumnos que ya existen pero fueron cambiados de grupo

        archivo = request.FILES.get('archivo')

        # Verificamos que el archivo tenga extensión CSV
        if not archivo.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser un CSV.')
            return redirect('importar_csv')

        # Intentamos decodificar el archivo primero como UTF-8, si falla, usamos Latin1
        try:
            contenido = archivo.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            archivo.seek(0)
            contenido = archivo.read().decode('latin1')

        # Convertimos el contenido a un flujo para el lector CSV
        io_string = io.StringIO(contenido)
        lector = csv.DictReader(io_string)

        # Iteramos sobre cada fila del archivo CSV
        for fila in lector:
            # Validamos que existan las columnas requeridas
            if 'Alumno/a' not in fila or 'Unidad' not in fila:
                messages.error(request, f"Columnas no válidas: {fila.keys()}")
                return redirect('importar_csv')

            nombre = fila['Alumno/a'].strip()
            unidad = fila['Unidad'].strip()

            # Si no hay unidad, rechazamos al alumno
            if unidad == '':
                alumnos_rechazados.append(nombre)
                continue

            # Intentamos dividir la unidad en "curso" y "letra"
            try:
                curso_str, letra = unidad.split('º ESO ')
                curso_str = f"{curso_str}º ESO"
                letra = letra.strip()
            except ValueError:
                alumnos_rechazados.append(nombre)
                continue

            # Obtenemos o creamos el curso y el grupo correspondiente
            curso, _ = Curso.objects.get_or_create(nivel=curso_str)
            grupo, _ = Grupo.objects.get_or_create(curso=curso, letra=letra)

            # Buscamos si ya existe un alumno con ese nombre
            alumno_existente = Alumno.objects.filter(nombre=nombre).first()

            if alumno_existente:
                if alumno_existente.grupo == grupo:
                    # Si el grupo es el mismo, es un duplicado
                    alumnos_duplicados.append(nombre)
                else:
                    # Si el grupo es distinto, lo actualizamos
                    alumno_existente.grupo = grupo
                    alumno_existente.save()
                    alumnos_cambiados.append(nombre)
            else:
                # Si no existe el alumno, lo creamos
                Alumno.objects.create(nombre=nombre, grupo=grupo)

        # Mensaje de éxito general
        messages.success(request, 'Alumnos importados correctamente.')

        # Renderizamos el template incluyendo todas las listas de resultados
        return render(request, 'alumnos/importar.html', {
            'alumnos_rechazados': alumnos_rechazados,
            'alumnos_duplicados': alumnos_duplicados,
            'alumnos_cambiados': alumnos_cambiados,
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