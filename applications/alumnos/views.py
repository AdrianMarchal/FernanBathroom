from django.shortcuts import render
import unicodedata
import csv
import io
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Func
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Grupo, Alumno, Curso
from ..historial.models import HistorialBathroom
from ..users.decorators import user_type_required


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class ImportarCSVView(View):
    def get(self, request):
        return render(request, 'alumnos/importar.html')

    def post(self, request):
        alumnos_rechazados = []
        alumnos_duplicados = []
        alumnos_cambiados = []

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
                letra = letra.strip()
            except ValueError:
                alumnos_rechazados.append(nombre)
                continue

            curso, _ = Curso.objects.get_or_create(nivel=curso_str)
            grupo, _ = Grupo.objects.get_or_create(curso=curso, letra=letra)

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

        messages.success(request, 'Alumnos importados correctamente.')
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


# Función personalizada para usar la extensión unaccent de PostgreSQL
class Unaccent(Func):
    function = 'unaccent'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador', 'profesor'), name='dispatch')
class ListarAlumnos(ListView):
    model = Alumno
    template_name = "alumnos/listar_alumnos.html"
    context_object_name = 'alumnos'
    paginate_by = 25

    def quitar_tildes(self, texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    def get_queryset(self):
        queryset = Alumno.objects.select_related('grupo__curso').order_by(
            'grupo__curso__nivel', 'grupo__letra', 'nombre'
        )

        nombre = self.request.GET.get('nombre')
        curso_id = self.request.GET.get('curso')
        grupo_id = self.request.GET.get('grupo')

        if nombre:
            palabras = self.quitar_tildes(nombre).strip().split()
            queryset = queryset.annotate(nombre_unaccent=Unaccent('nombre'))
            for palabra in palabras:
                queryset = queryset.filter(nombre_unaccent__icontains=palabra)

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
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes

        estadisticas = {}
        for alumno in context['alumnos']:
            tramo1 = HistorialBathroom.objects.filter(
                alumno=alumno,
                hora__gte=timezone.datetime.combine(hoy, timezone.datetime.strptime('08:00', '%H:%M').time()).time(),
                hora__lte=timezone.datetime.combine(hoy, timezone.datetime.strptime('11:00', '%H:%M').time()).time()
            ).count()

            tramo2 = HistorialBathroom.objects.filter(
                alumno=alumno,
                hora__gt=timezone.datetime.combine(hoy, timezone.datetime.strptime('11:00', '%H:%M').time()).time(),
                hora__lte=timezone.datetime.combine(hoy, timezone.datetime.strptime('15:00', '%H:%M').time()).time()
            ).count()

            semana = HistorialBathroom.objects.filter(
                alumno=alumno,
                hora__isnull=False,
                fecha__range=(inicio_semana, hoy)
            ).count()

            estadisticas[alumno.id] = {
                'tramo1': tramo1,
                'tramo2': tramo2,
                'semana': semana,
            }

        context['estadisticas'] = estadisticas
        return context
