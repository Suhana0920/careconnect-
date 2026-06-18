from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if not hasattr(request.user, 'profile'):
                return redirect('login')
            user_role = request.user.profile.role
            if user_role not in allowed_roles:
                if user_role == 'patient':
                    return redirect('dashboard')
                elif user_role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user_role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator 