from django.shortcuts import render, redirect
from .models import KodeUser
from .decorators import *
from hashlib import sha256


@check_session
def base(request):
    params = {
        'auth': request.session['auth'],
    }
    return render(request, 'base.html', params)


@check_session
def index(request):
    if request.session['auth'] == 1:
        params = {
            'auth': request.session['auth'],
        }
        return render(request, 'index.html', params)
    else:
        return redirect('login')


@check_session
def panel(request):
    if request.method == 'POST':
        if request.session['auth'] == 1:
            error_mess = ''
            cool_news = ''
            user_data = KodeUser.objects.get(id=request.session['id'])
            if user_data.password == sha256(bytes(request.POST['curr_pass'], 'utf-8')).hexdigest():
                if request.POST['new_pass'] != '':
                    if request.POST['confirm_pass'] != '':
                        if request.POST['new_pass'] == request.POST['confirm_pass']:
                            if user_data.password != sha256(bytes(request.POST['confirm_pass'], 'utf-8')).hexdigest():
                                user_data.password = sha256(bytes(request.POST['confirm_pass'], 'utf-8')).hexdigest()
                                user_data.save()
                                cool_news = 'Данные успешно изменены'
                            else:
                                error_mess = 'Вы не можете указать свой текущий пароль'
                        else:
                            error_mess = 'Повторный пароль введён неверно'
                    else:
                        error_mess = 'Введите пароль повторно'
                else:
                    pass

                if request.POST['email'] != user_data.email:
                    user_data.email = request.POST['email']  # Change email
                    user_data.save()
                    cool_news = 'Данные успешно изменены'
                else:
                    pass

                if request.POST['nickname'] != user_data.username:
                    user = KodeUser.objects.filter(username=request.POST['nickname']).exists()
                    if user is False:
                        user_data.username = request.POST['nickname']  # Change username
                        user_data.save()
                        cool_news = 'Данные успешно изменены'
                    else:
                        error_mess = 'Такой юзер уже есть'
                else:
                    pass
            else:
                error_mess = "Неверно введён пароль"
            params = {
                'name': user_data.username,
                'email': user_data.email,
                'error_message': error_mess,
                'cool_mess': cool_news,
            }
            return render(request, 'panel.html', params)
        else:
            return redirect('login')
    else:
        if request.session['auth'] == 1:
            user_data = KodeUser.objects.get(id=request.session['id'])
            params = {
                'auth': request.session['auth'],
                'name': user_data.username,
                'email': user_data.email,
                'password': user_data.password,
            }
            return render(request, 'panel.html', params)
        else:
            return redirect('login')


@check_session
def login(request):
    if request.method == 'GET':
        params = {
            'auth': request.session['auth'],
        }
        return render(request, 'login.html', params)
    else:
        login = request.POST['login']
        password_hash = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
        try:
            user = KodeUser.objects.get(username=login)
        except Exception as e:
            print(e)
            params = {
                'error': 'Не удалось авторизоваться'
            }
            return render(request, 'login.html', params)
        else:
            if password_hash == user.password:
                request.session['auth'] = 1
                request.session['id'] = user.id
                return redirect('index')
            else:
                params = {
                    'error': 'Не удалось авторизоваться',
                }
                return render(request, 'login.html', params)


@check_session
def logout(request):
    request.session['auth'] = 0
    return redirect('login')


def firsttime(request):
    params = {
        'error': '',
    }
    if request.method == 'POST':
        code = request.POST['code']
        try:
            user_data = KodeUser.objects.get(invitation_code=code)
            if request.POST['confirm_password'] == request.POST['password']:
                user_data.password = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
                user_data.invitation_code = ''
                user_data.save()
            else:
                params = {
                    'error': 'the second password is not correctly entered',
                }
                return render(request, 'firsttime.html', params)
        except Exception as e:
            params = {
                'error': 'incorrect invitation code',
            }
            return render(request, 'firsttime.html', params)
        return redirect('login')
    return render(request, 'firsttime.html', params)

# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(gen(Camera),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
