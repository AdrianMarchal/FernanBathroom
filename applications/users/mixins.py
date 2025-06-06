from django.shortcuts import redirect
from django.urls import reverse_lazy


# Mixin que impide a usuarios autenticados acceder a ciertas vistas (como la de login o registro)
class AnonymousRequiredMixin:
    def get_redirect_url(self):
        user = self.request.user
        # Si el usuario no está autenticado, no se necesita redirigir
        if not user.is_authenticated:
            return None

        # Redirige a la home según tipo de usuario
        if user.type_user_per == 'administrador':
            return reverse_lazy('home_app:homeAdmin')
        elif user.type_user_per == 'conserje':
            return reverse_lazy('home_app:homeConserje')
        elif user.type_user_per == 'profesor':
            return reverse_lazy('home_app:home')
        return reverse_lazy('login')  # fallback

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario está autenticado, redirige a su página de inicio
        if request.user.is_authenticated:
            redirect_url = self.get_redirect_url()
            if redirect_url:
                return redirect(redirect_url)

        # Si no está autenticado, continúa con el flujo normal
        return super().dispatch(request, *args, **kwargs)
