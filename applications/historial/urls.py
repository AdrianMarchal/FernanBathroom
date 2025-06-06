from django.urls import path
from . import views

# urls.py
urlpatterns = [
    #URL para la vista encargada de guardar el registro del baño de un alumno esta tiene que recibir el id valido de un alumno
    path('add_historial/<int:alumno_id>/', views.CrearHistorialBathroom.as_view(), name='crear_historial'),
]
