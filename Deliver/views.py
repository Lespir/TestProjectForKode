from django.shortcuts import render, redirect
from .decorators import *
from hashlib import sha256
from KODE.models import Order


# Create your views here.


@check_session_cour
def cour_login(request):  # system of login
    if request.method == 'GET':
        error = ''
        return render(request, 'deliver/login.html')
    else:
        login = request.POST['login']
        password_hash = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
        try:
            user = Courier.objects.get(nickname=login)  # trying to get user with this name
        except Exception as e:
            error = 'Failed to authenticate'
            return render(request, 'deliver/login.html', {'error': error})
        else:  # if user had found, change him session auth 0 as 1
            if password_hash == user.password:
                request.session['auth'] = 1
                request.session['id'] = user.id
                return redirect('orders')
            else:
                error = 'Failed to authenticate'
                return render(request, 'deliver/login.html', {'error': error})


@check_session_cour
def cour_first_time(request):  # if user has not account, he should create it with help a special code
    error = ''
    if request.method == 'POST':
        code = request.POST['code']
        nickname = request.POST['nickname']
        try:
            user_data = Courier.objects.get(invitation_code=code)
            if not Courier.objects.filter(nickname=nickname):
                if request.POST['confirm_password'] == request.POST['password']:
                    user_data.password = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
                    user_data.invitation_code = ''
                    user_data.nickname = nickname
                    user_data.save()
                    return redirect('cour_login')
                else:
                    error = 'The second password is not correctly entered'
            else:
                error = 'Nickname is already taken'
        except Exception as e:
            error = 'Incorrect invitation code'
    return render(request, 'deliver/firsttime.html', {'error': error})


@check_session_cour
def cour_logout(request):
    request.session['auth'] = 0
    return redirect('cour_login')


@check_session_cour
@login_require_cour
def orders(request):  # management order
    try:
        courier_orders = Order.objects.filter(courier=request.session['id'])
        print(courier_orders)
        return render(request, 'deliver/orders.html', {'auth': request.session['auth'],
                                                       'orders': courier_orders})
    except Exception as e:
        return render(request, 'deliver/orders.html', {'auth': request.session['auth']})


def order_info(request):
    order_id = request.path_info.split('/')[-1]
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        order.status = request.POST.get('button')
        order.save()
    order = Order.objects.get(id=order_id)
    return render(request, 'deliver/order_status.html', {'order': order})


@check_session_cour
@login_require_cour
def cour_panel(request):  # panel for changing personal data
    if request.method == 'POST':
        error_mess = ''
        cool_news = ''
        user_data = Courier.objects.get(id=request.session['id'])  # get user object from db
        if user_data.password == sha256(
                bytes(request.POST['curr_pass'], 'utf-8')).hexdigest():
            if request.POST['new_pass'] != '':
                if request.POST['confirm_pass'] != '':
                    if request.POST['new_pass'] == request.POST['confirm_pass']:
                        if user_data.password != sha256(
                                bytes(request.POST['confirm_pass'], 'utf-8')).hexdigest():  # change the password
                            user_data.password = sha256(bytes(request.POST['confirm_pass'], 'utf-8')).hexdigest()
                            user_data.save()
                            cool_news = 'Data successfully changed'
                        else:
                            error_mess = 'You cant specify your current password'
                    else:
                        error_mess = 'The second password is not correctly entered'
                else:
                    error_mess = 'Entered the second password'
            else:
                pass

            if request.POST['nickname'] != user_data.nickname:
                user = Courier.objects.filter(nickname=request.POST['nickname']).exists()
                if user is False:
                    user_data.nickname = request.POST['nickname']  # Change nickname
                    user_data.save()
                    cool_news = 'Data successfully changed'
                else:
                    error_mess = 'Such user already exists'
            else:
                pass
        else:
            error_mess = "Password was incorrectly entered"
        params = {
            'name': user_data.nickname,
            'error_message': error_mess,
            'cool_mess': cool_news,
        }
        return render(request, 'deliver/panel.html', params)
    else:
        user_data = Courier.objects.get(id=request.session['id'])
        params = {
            'auth': request.session['auth'],
            'name': user_data.nickname,
            'password': user_data.password,
        }
        return render(request, 'deliver/panel.html', params)
