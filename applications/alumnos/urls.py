# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('importar/', views.importar_csv, name='importar_csv'),
    path('borrar/', views.borrar_datos, name='borrar_datos'),
]
