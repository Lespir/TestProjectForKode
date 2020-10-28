from django.shortcuts import render, redirect
from .models import Manager, Product, Order, Courier
from .decorators import *
from hashlib import sha256
from mega import Mega
import random

mega = Mega()


@check_session
def base(request):  # market page
    products = Product.objects.all()
    return render(request, 'market.html', {'auth': request.session['auth'],
                                           'products': products})


@check_session
@login_require
def index(request):  # management order
    orders = Order.objects.all()
    return render(request, 'manage.html', {'auth': request.session['auth'],
                                           'orders': orders})


@check_session
@login_require
def panel(request):  # panel for changing personal data
    if request.method == 'POST':
        error_mess = ''
        cool_news = ''
        user_data = Manager.objects.get(id=request.session['id'])  # get user object from db
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

            if request.POST['email'] != user_data.email:
                user_data.email = request.POST['email']  # Change email
                user_data.save()
                cool_news = 'Data successfully changed'
            else:
                pass

            if request.POST['nickname'] != user_data.nickname:
                user = Manager.objects.filter(nickname=request.POST['nickname']).exists()
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
            'email': user_data.email,
            'error_message': error_mess,
            'cool_mess': cool_news,
        }
        return render(request, 'panel.html', params)
    else:
        user_data = Manager.objects.get(id=request.session['id'])
        params = {
            'auth': request.session['auth'],
            'name': user_data.nickname,
            'email': user_data.email,
            'password': user_data.password,
        }
        return render(request, 'panel.html', params)


@check_session
def login(request):  # system of login
    if request.method == 'GET':
        return render(request, 'login.html', {'auth': request.session['auth']})
    else:
        login = request.POST['login']
        password_hash = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
        try:
            user = Manager.objects.get(nickname=login)  # trying to get user with this name
        except Exception as e:
            error = 'Failed to authenticate'
            return render(request, 'login.html', {'error': error})
        else:   # if user had found, change him session auth 0 as 1
            if password_hash == user.password:
                request.session['auth'] = 1
                request.session['id'] = user.id
                return redirect('index')
            else:
                error = 'Failed to authenticate'
                return render(request, 'login.html', {'error': error})


@check_session
def logout(request):
    request.session['auth'] = 0
    return redirect('login')


@check_session
def first_time(request):   # if user has not account, he should create it with help a special code
    error = ''
    if request.method == 'POST':
        code = request.POST['code']
        nickname = request.POST['nickname']
        try:
            user_data = Manager.objects.get(invitation_code=code)
            if not Manager.objects.filter(nickname=nickname):
                if request.POST['confirm_password'] == request.POST['password']:
                    user_data.password = sha256(bytes(request.POST['password'], 'utf-8')).hexdigest()
                    user_data.invitation_code = ''
                    user_data.nickname = nickname
                    user_data.save()
                    return redirect('login')
                else:
                    error = 'The second password is not correctly entered'
            else:
                error = 'Nickname is already taken'
        except Exception as e:
            error = 'Incorrect invitation code'
    return render(request, 'firsttime.html', {'error': error})


@check_session
@login_require
def add_product(request):
    error = ''
    cool_mess = ''
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        count = request.POST['count']
        if not Product.objects.filter(title=title):
            if not request.FILES:
                product = Product.objects.create(title=title,
                                                 description=description,
                                                 count=count)
                product.save()
                cool_mess = 'Product successfully added'
            else:
                try:
                    # image = request.FILES['file']
                    # file_path = f'KODE/temp_media/{image.name}'
                    # with open(file_path, 'wb') as f:   # temp save image
                    #     for chunk in image.chunks():
                    #         f.write(chunk)
                    # m = mega.login('email', 'password')
                    # folder = m.find('KODE')
                    # file = m.upload(file_path, folder[0])   # upload image to MEGA
                    product = Product.objects.create(title=title, description=description,
                                                     count=count)
                    # I will add it, when i started user drive (Mega or Google)
                    product.save()
                    # os.remove(file_path)
                    cool_mess = 'Product successfully added'
                except Exception as e:
                    error = 'Failed to add product'
        else:
            error = 'Product name already exists'
    return render(request, 'add_product.html', {'error': error, 'cool_mess': cool_mess})


def product_info(request):
    name = request.path_info.split('/')[-1]
    product = Product.objects.get(title=name)
    if request.method == 'POST':
        name_of_user = request.POST['name_of_user']
        address = request.POST['address']
        phone = request.POST['phone']
        count = request.POST['quantity']
        if product.count < int(count):
            error = 'Not enough products in the storage'
            return render(request, 'product.html',
                          {'error': error, 'product': product, 'auth': request.session['auth']})
        else:
            order = Order.objects.create(title=name, phone=phone, name_of_user=name_of_user, count=count, courier=0,
                                         address=address, district=random.randint(1, 2))
            order.save()
            Product.objects.filter(title=name).update(count=product.count - int(count))
            return redirect('base')
    product = Product.objects.get(title=name)
    try:
        return render(request, 'product.html', {'product': product, 'auth': request.session['auth']})
    except Exception as e:
        return redirect('base')


@check_session
@login_require
def order_info(request):
    order_id = request.path_info.split('/')[-1]
    order = Order.objects.get(id=order_id)
    try:
        couriers = Courier.objects.filter(district=order.district)
    except Exception as e:
        couriers = ''
    if request.POST.get('courier'):
        order.courier = request.POST.get('courier')
        order.save()
    elif request.POST.get('status'):
        order.status = request.POST.get('status')
        order.save()
    order = Order.objects.get(id=order_id)
    try:
        order_courier = Courier.objects.get(id=order.courier)
        order_courier = order_courier.name
    except Exception as e:
        order_courier = ''
    if order.status == 0:
        status = 'Passed'  # Принят
    elif order.status == 1:
        status = 'Delivering'  # Доставляется
    elif order.status == 2:
        status = 'Delivered'  # Доставлен
    elif order.status == 3:
        status = 'Did not deliver'  # Не даставлен
    else:
        status = ''
    return render(request, 'order_info.html',
                  {'order': order, 'status': status, 'couriers': couriers, 'order_courier': order_courier})
