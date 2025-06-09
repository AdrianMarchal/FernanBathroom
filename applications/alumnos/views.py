from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Func, Count, Q
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView

import csv
import io
import unicodedata
from datetime import timedelta


from .models import Grupo, Alumno, Curso
from ..historial.models import HistorialBathroom
from ..users.decorators import user_type_required  # Decorador personalizado para verificar el tipo de usuario


# Vista para importar alumnos desde un archivo CSV
@method_decorator(login_required, name='dispatch')  # Requiere que el usuario esté autenticado
@method_decorator(user_type_required('administrador'), name='dispatch')  # Requiere que el usuario sea administrador
class ImportarCSVView(View):

    def get(self, request):
        # Muestra el formulario de importación
        return render(request, 'alumnos/importar.html')

    def post(self, request):
        # Maneja la lógica de importación de datos desde el CSV
        alumnos_rechazados = []   # Alumnos que no se pudieron importar por errores
        alumnos_duplicados = []   # Alumnos que ya existen en la base de datos con el mismo grupo
        alumnos_cambiados = []    # Alumnos que ya existían pero se les cambió el grupo

        archivo = request.FILES.get('archivo')  # Archivo subido por el usuario

        #Se comprueba que el archivo sea un CSV en caso de que no sea asi
        # se lanza un error y se le indica al usuario
        if not archivo.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser un CSV.')
            return redirect('importar_csv')

        # Intenta decodificar el archivo en UTF-8 o Latin1 si falla
        try:
            contenido = archivo.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            archivo.seek(0)
            contenido = archivo.read().decode('latin1')

        io_string = io.StringIO(contenido)
        lector = csv.DictReader(io_string)  # Lee el CSV como diccionario

        for fila in lector:
            if 'Alumno/a' not in fila or 'Unidad' not in fila:
                # Validación de columnas
                messages.error(request, f"Columnas no válidas: {fila.keys()}")
                return redirect('importar_csv')

            nombre = fila['Alumno/a'].strip()
            unidad = fila['Unidad'].strip()

            if unidad == '':
                alumnos_rechazados.append(nombre)
                continue

            # Intenta separar el curso y la letra (por ejemplo, "1º ESO A")
            try:
                curso_str, letra = unidad.split('º ESO ')
                curso_str = f"{curso_str}º ESO"
                letra = letra.strip()
            except ValueError:
                alumnos_rechazados.append(nombre)
                continue

            # Crea o recupera el curso y grupo correspondientes
            curso, _ = Curso.objects.get_or_create(nivel=curso_str)
            grupo, _ = Grupo.objects.get_or_create(curso=curso, letra=letra)

            # Revisa si el alumno ya existe
            alumno_existente = Alumno.objects.filter(nombre=nombre).first()

            if alumno_existente:
                if alumno_existente.grupo == grupo:
                    alumnos_duplicados.append(nombre)
                else:
                    alumno_existente.grupo = grupo
                    alumno_existente.save()
                    alumnos_cambiados.append(nombre)
            else:
                Alumno.objects.create(nombre=nombre, grupo=grupo)

        # Muestra resultados de la importación
        messages.success(request, 'Alumnos importados correctamente.')
        return render(request, 'alumnos/importar.html', {
            'alumnos_rechazados': alumnos_rechazados,
            'alumnos_duplicados': alumnos_duplicados,
            'alumnos_cambiados': alumnos_cambiados,
        })


# Vista para borrar todos los datos de alumnos, grupos y cursos
@method_decorator(login_required, name='dispatch')# Requiere que el usuario esté autenticado
@method_decorator(user_type_required('administrador'), name='dispatch')# Requiere que el usuario sea administrador
class BorrarDatosView(View):
    def get(self, request):
        # Página de confirmación
        return render(request, 'alumnos/borrar_confirmacion.html')

    def post(self, request):
        # Elimina todos los datos de alumnos, grupos y cursos
        Alumno.objects.all().delete()
        Grupo.objects.all().delete()
        Curso.objects.all().delete()
        messages.success(request, 'Todos los datos han sido eliminados correctamente.')
        return redirect('importar_csv')


# Función personalizada para aplicar la función unaccent de PostgreSQL (elimina tildes)
class Unaccent(Func):
    function = 'unaccent'


# Vista para listar los alumnos con filtros y estadísticas semanales
@method_decorator(login_required, name='dispatch') # Requiere que el usuario esté autenticado
@method_decorator(user_type_required('administrador', 'profesor', 'conserje'), name='dispatch') # Disponible para cualquier usuario registrado
class ListarAlumnos(ListView):
    model = Alumno
    template_name = "alumnos/listar_alumnos.html"
    context_object_name = 'alumnos'
    paginate_by = 25  # Paginación de 25 alumnos por página

    # Función auxiliar para quitar tildes de un texto
    def quitar_tildes(self, texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    def get_queryset(self):
        # Consulta principal para filtrar y ordenar alumnos
        queryset = Alumno.objects.select_related('grupo__curso').order_by(
            'grupo__curso__nivel', 'grupo__letra', 'nombre'
        )
        print("Alumnos")
        print(queryset)

        # Filtros desde la URL
        nombre = self.request.GET.get('nombre')
        curso_id = self.request.GET.get('curso')
        grupo_id = self.request.GET.get('grupo')

        # Filtro por nombre (ignorando tildes)
        if nombre:
            palabras = self.quitar_tildes(nombre).strip().split()
            queryset = queryset.annotate(nombre_unaccent=Unaccent('nombre'))
            for palabra in palabras:
                queryset = queryset.filter(nombre_unaccent__icontains=palabra)

        # Filtro por curso y grupo
        if curso_id:
            queryset = queryset.filter(grupo__curso__id=curso_id)
        if grupo_id:
            queryset = queryset.filter(grupo__id=grupo_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cursos'] = Curso.objects.all().order_by('nivel')
        context['grupos'] = Grupo.objects.select_related('curso').order_by('curso__nivel', 'letra')

        hoy = timezone.localtime().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())

        alumno_ids = [a.id for a in context['alumnos']]

        # Obtener los conteos agrupados para todos los alumnos paginados en una consulta
        registros = HistorialBathroom.objects.filter(
            alumno_id__in=alumno_ids,
            fecha__range=(inicio_semana, hoy),
        ).exclude(tramo=0).values('alumno_id').annotate(
            tramo1_count=Count('id', filter=Q(tramo=1, fecha=hoy)),
            tramo2_count=Count('id', filter=Q(tramo=2, fecha=hoy)),
            semana_count=Count('id'),
        )

        estadisticas = {r['alumno_id']: {
            'tramo1': r['tramo1_count'],
            'tramo2': r['tramo2_count'],
            'semana': r['semana_count'],
        } for r in registros}

        context['estadisticas'] = estadisticas

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class EditarNecesidadMedicaView(View):
    def post(self, request, alumno_id):
        alumno = get_object_or_404(Alumno, id=alumno_id)
        alumno.necesidad_medica = 'necesidad_medica' in request.POST
        alumno.save()
        return redirect(request.META.get('HTTP_REFERER', 'listar_alumnos'))
