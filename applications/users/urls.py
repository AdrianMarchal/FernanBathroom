from django.urls import path
from . import views
from .views import permission_denied_redirect

app_name = 'users_app'

urlpatterns = [
    path(
        'registerUser/',
        views.UserRegisterView.as_view(),
        name='registerUser'),
    path(
        'listar_usuarios/',
        views.UserListView.as_view(),
        name='listar_usuarios'),

    path(
        'login/',
        views.LoginView.as_view(),
        name='userLogin'),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='userLogout'),
    path(
        'error-permiso/',
        permission_denied_redirect,
        name='permission_denied')
]
