from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import  reverse_lazy

from applications.users.decorators import user_type_required


# Create your views here.


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('profesor'), name='dispatch')
class HomePageView(LoginRequiredMixin,TemplateView):
    template_name = "homes/home.html"
    login_url = reverse_lazy("users_app:userLogin")


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('conserje'), name='dispatch')
class HomeConserjeView(TemplateView):
    template_name = "homes/home_conserje.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(user_type_required('administrador'), name='dispatch')
class HomeAdminView(TemplateView):
    template_name = "homes/home_admin.html"




