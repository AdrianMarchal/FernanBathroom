# applications/users/decorators.py
from functools import wraps
from django.shortcuts import redirect


# Decorador personalizado para restringir el acceso a vistas según el tipo de usuario
def user_type_required(*expected_types):
    # Esta función es el decorador real que envuelve la vista
    def decorator(view_func):
        @wraps(view_func)  # Preserva los atributos originales de la función decorada
        def _wrapped_view(request, *args, **kwargs):
            # Verifica si el usuario ha iniciado sesión
            if not request.user.is_authenticated:
                return redirect('users_app:userLogin')  # Redirige al login si no está autenticado

            # Verifica si el tipo de usuario está permitido
            if request.user.type_user_per not in expected_types:
                return redirect('users_app:permission_denied')  # Redirige a página de permiso denegado

            # Si el usuario está autenticado y tiene el tipo correcto, ejecuta la vista
            return view_func(request, *args, **kwargs)

        return _wrapped_view  # Devuelve la vista decorada

    return decorator  # Devuelve el decorador