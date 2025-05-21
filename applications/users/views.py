from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse


from applications.users.forms import UserRegisterForm, LoginForm
from applications.users.models import User


# Create your views here.



class UserRegisterView(FormView):
    template_name = "user/admin/registrarProfesor.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
            type_user="profesor",
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
        )
        return super(UserRegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginView,self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(
            reverse("users:login")
        )