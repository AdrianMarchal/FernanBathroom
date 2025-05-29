from django.urls import path
from . import views

# urls.py
urlpatterns = [
    path('add_historial/<int:alumno_id>/', views.CrearHistorialBathroom.as_view(), name='crear_historial'),
]
