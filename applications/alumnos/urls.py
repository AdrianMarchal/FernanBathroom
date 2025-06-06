# urls.py
from django.urls import path
from . import views
from .views import ListarAlumnos


#URL de la aplicacion
urlpatterns = [
    #URL para la vista encargada de importar los alumnos desde un csv
    path('importar/', views.ImportarCSVView.as_view(), name='importar_csv'),
    #URL para la vista encargada de borrar todos los datos de la aplicacion
    path('borrar/', views.BorrarDatosView.as_view(), name='borrar_datos'),
    #URL para la vista encargada de listar todos los alumnos
    path('listar_alumnos/', ListarAlumnos.as_view(), name='listar_alumnos'),


]
