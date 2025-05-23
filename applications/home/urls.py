

from django.urls import path
from . import views

app_name = 'home_app'

urlpatterns = [
    path(
        'home/',
        views.HomePageView.as_view(),
        name='home'),
    path(
        'home_conserje/',
        views.HomeConserjeView.as_view(),
        name='homeConserje'),
    path(
        'home_administrador/',
        views.HomeAdminView.as_view(),
        name='homeAdmin'),
]
