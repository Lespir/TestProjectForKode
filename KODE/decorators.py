import datetime
from django.shortcuts import redirect
from .models import Manager


def check_session(func):
    def decorator(*args, **kwargs):
        if 'auth' not in args[0].session.keys():
            args[0].session['auth'] = 0
        if 'id' not in args[0].session.keys():
            args[0].session['id'] = None
        return func(*args, **kwargs)
    return decorator


def login_require(func):
    def decorator(*args, **kwargs):
        if args[0].session.get('auth'):
            try:
                Manager.objects.get(id=args[0].session['id'])
            except Exception as e:
                print(e)
                args[0].session['auth'] = 0
                return redirect('login')
            else:
                return func(*args, **kwargs)
        return redirect('login')
    return decorator
