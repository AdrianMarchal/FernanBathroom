from django.shortcuts import render

# Create your views here.

# views.py
import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Grupo, Alumno, Curso


import csv
import io

def importar_csv(request):
    alumnos_rechazados = []

    if request.method == 'POST':
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
            _, creado = Alumno.objects.get_or_create(nombre=nombre, grupo=grupo)

        messages.success(request, 'Alumnos importados correctamente.')

    return render(request, 'alumnos/importar.html', {'alumnos_rechazados': alumnos_rechazados})



def borrar_datos(request):
    if request.method == 'POST':
        Alumno.objects.all().delete()
        Grupo.objects.all().delete()
        Curso.objects.all().delete()
        messages.success(request, 'Todos los datos han sido eliminados correctamente.')
        return redirect('importar_csv')  # O redirige a donde prefieras

    return render(request, 'alumnos/borrar_confirmacion.html')