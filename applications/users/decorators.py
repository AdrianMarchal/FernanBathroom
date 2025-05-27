# applications/users/decorators.py
from functools import wraps
from django.shortcuts import redirect

def user_type_required(*expected_types):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users_app:userLogin')
            if request.user.type_user_per not in expected_types:
                return redirect('users_app:permission_denied')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
