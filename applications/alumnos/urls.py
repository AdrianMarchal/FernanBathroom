# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('importar/', views.ImportarCSVView.as_view(), name='importar_csv'),
    path('borrar/', views.BorrarDatosView.as_view(), name='borrar_datos'),
]
