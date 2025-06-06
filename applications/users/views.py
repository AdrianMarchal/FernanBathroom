from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, ListView
from django.urls import reverse, reverse_lazy

from applications.users.decorators import user_type_required
from applications.users.forms import UserRegisterForm, LoginForm
from applications.users.mixins import AnonymousRequiredMixin
from applications.users.models import User
from django.contrib import messages


# Create your views here.


@method_decorator(login_required, name='dispatch')  # Solo usuarios logueados
@method_decorator(user_type_required('administrador'), name='dispatch')  # Solo usuarios tipo "administrador"
class UserRegisterView(FormView):
    template_name = "user/admin/registrar_usuario.html"  # Plantilla HTML
    form_class = UserRegisterForm  # Formulario que se usará
    success_url = reverse_lazy("users_app:registerUser")  # Redirección al registrarse correctamente

    # Metodo que se ejecuta si el formulario es válido
    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Verifica que no exista un usuario con ese email
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Ya existe un usuario con este correo.')
            return self.form_invalid(form)

        # Crea el nuevo usuario con los datos del formulario
        User.objects.create_user(
            email=email,
            password=form.cleaned_data['password1'],
            type_user=form.cleaned_data['type_user'],  # profesor o conserje
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
        )
        messages.success(self.request, "Usuario registrado exitosamente.")  # Mensaje de éxito
        return super().form_valid(form)


class LoginView(AnonymousRequiredMixin, FormView):  # Usa mixin para evitar que usuarios logueados entren
    template_name = 'user/login.html'
    form_class = LoginForm


    def form_valid(self, form):
        # Autentica al usuario
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)  # Inicia sesión
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        # Redirige a la página principal según el tipo de usuario
        user = self.request.user
        if user.type_user_per == 'administrador':
            return reverse_lazy('home_app:homeAdmin')
        elif user.type_user_per == 'conserje':
            return reverse_lazy('home_app:homeConserje')
        elif user.type_user_per == 'profesor':
            return reverse_lazy('home_app:home')
        else:
            return reverse_lazy('login')  # Redirección por defecto



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Cierra sesión del usuario
        return HttpResponseRedirect(reverse("users_app:userLogin"))  # Redirige al login


def permission_denied_redirect(request):
    return render(request, "errors/permission_denied.html")  # Muestra una plantilla de error



@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = "user/admin/listar_usuario.html"
    context_object_name = 'users'

    def get_queryset(self):
        # Excluye usuarios especiales tipo 'SuperUsuarioRoot' de la lista
        return User.objects.exclude(type_user_per='SuperUsuarioRoot')