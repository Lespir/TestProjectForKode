from django.shortcuts import redirect
from KODE.models import Courier


def check_session_cour(func):
    def decorator(*args, **kwargs):
        if 'auth' not in args[0].session.keys():
            args[0].session['auth'] = 0
        if 'id' not in args[0].session.keys():
            args[0].session['id'] = None
        return func(*args, **kwargs)
    return decorator


def login_require_cour(func):
    def decorator(*args, **kwargs):
        if args[0].session.get('auth'):
            try:
                Courier.objects.get(id=args[0].session['id'])
            except Exception as e:
                print(e)
                args[0].session['auth'] = 0
                return redirect('cour_login')
            else:
                return func(*args, **kwargs)
        return redirect('cour_login')
    return decorator
