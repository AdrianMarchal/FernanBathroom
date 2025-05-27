# urls.py
from django.urls import path
from . import views
from .views import ListarAlumnos

urlpatterns = [
    path('importar/', views.ImportarCSVView.as_view(), name='importar_csv'),
    path('borrar/', views.BorrarDatosView.as_view(), name='borrar_datos'),
    path('listar_alumnos/', ListarAlumnos.as_view(), name='listar_alumnos'),
]
