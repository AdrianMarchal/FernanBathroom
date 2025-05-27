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


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class UserRegisterView(FormView):
    template_name = "user/admin/registrar_usuario.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users_app:registerUser")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Ya existe un usuario con este correo.')
            return self.form_invalid(form)

        User.objects.create_user(
            email=email,
            password=form.cleaned_data['password1'],
            type_user=form.cleaned_data['type_user'],  # profesor o conserje
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
        )
        messages.success(self.request, "Usuario registrado exitosamente.")
        return super().form_valid(form)



class LoginView(AnonymousRequiredMixin, FormView):
    template_name = 'user/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginView,self).form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.type_user_per == 'administrador':
            return reverse_lazy('home_app:homeAdmin')
        elif user.type_user_per == 'conserje':
            return reverse_lazy('home_app:homeConserje')
        elif user.type_user_per == 'profesor':
            return reverse_lazy('home_app:home')
        else:
            return reverse_lazy('login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(
            reverse("users_app:userLogin")
        )

def permission_denied_redirect(request):
    return render(request, "errors/permission_denied.html")


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = "user/admin/listar_usuario.html"
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(type_user_per='SuperUsuarioRoot')