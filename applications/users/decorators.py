# applications/users/decorators.py
from django.shortcuts import redirect

def user_type_required(expected_type):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users_app:userLogin')
            if request.user.type_user_per != expected_type:
                return redirect('users_app:permission_denied')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

