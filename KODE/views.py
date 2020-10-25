from django.shortcuts import render, redirect
from .models import KodeUser, Product, Order, Courier
from .decorators import *
from hashlib import sha256
from mega import Mega
import os

mega = Mega()


@check_session
def base(request):  # market page
    products = Product.objects.all()
    params = {
        'auth': request.session['auth'],
        'products': products,
    }
    return render(request, 'market.html', params)


@check_session
@login_require
def index(request):  # management order
    params = {
        'auth': request.session['auth'],
        'l': (5, 6, 7, 8),
    }
    return render(request, 'manage.html', params)


@check_session
@login_require
def panel(request):  # panel for changing personal data
    if request.method == 'POST':
        error_mess = ''
        cool_news = ''
        user_data = KodeUser.objects.get(id=request.session['id'])  # get user object from db
        if user_data.password == sha256(
                bytes(request.POST['curr_pass'], 'utf-8')).hexdigest():
            if request.POST['new_pass'] != '':
                if request.POST['confirm_pass'] != '':
                    if request.POST['new_pass'] == request.POST['confirm_pass']:
                        if user_data.password != sha256(bytes(request.POST['confirm_pass'], 'utf-8')).hexdigest():
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

            if request.POST['nickname'] != user_data.username:
                user = KodeUser.objects.filter(username=request.POST['nickname']).exists()
                if user is False:
                    user_data.username = request.POST['nickname']  # Change username
                    user_data.save()
                    cool_news = 'Data successfully changed'
                else:
                    error_mess = 'Such user already exists'
            else:
                pass
        else:
            error_mess = "Password was incorrectly entered"
        params = {
            'name': user_data.username,
            'email': user_data.email,
            'error_message': error_mess,
            'cool_mess': cool_news,
        }
        return render(request, 'panel.html', params)
    else:
        user_data = KodeUser.objects.get(id=request.session['id'])
        params = {
            'auth': request.session['auth'],
            'name': user_data.username,
            'email': user_data.email,
            'password': user_data.password,
        }
        return render(request, 'panel.html', params)


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
                'error': 'Failed to authenticate'
            }
            return render(request, 'login.html', params)
        else:
            if password_hash == user.password:
                request.session['auth'] = 1
                request.session['id'] = user.id
                return redirect('index')
            else:
                params = {
                    'error': 'Failed to authenticate',
                }
                return render(request, 'login.html', params)


@check_session
def logout(request):
    request.session['auth'] = 0
    return redirect('login')


@check_session
def first_time(request):
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
                    'error': 'The second password is not correctly entered',
                }
                return render(request, 'firsttime.html', params)
        except Exception as e:
            params = {
                'error': 'Incorrect invitation code',
            }
            return render(request, 'firsttime.html', params)
        return redirect('login')
    return render(request, 'firsttime.html', params)


@check_session
@login_require
def add_product(request):
    params = {
        'error': '',
    }
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        count = request.POST['count']
        if not request.FILES:
            product = Product.objects.create(title=title,
                                             description=description,
                                             count=count)
            product.save()
            params = {
                'cool_mess': 'Product successfully added',
            }
        else:
            try:
                # image = request.FILES['file']
                # file_path = f'KODE/temp_media/{image.name}'
                # with open(file_path, 'wb') as f:   # temp save image
                #     for chunk in image.chunks():
                #         f.write(chunk)
                # m = mega.login('alecsey.o.nikitin@gmail.com', '62195111aon$')
                # folder = m.find('KODE')
                # file = m.upload(file_path, folder[0])   # upload image to MEGA
                product = Product.objects.create(title=title, description=description,
                                                 count=count)   # image='https://mega.nz/file/' + m.get_upload_link(file).split('#!')[1]
                                                                # I will add it, when i started user drive (Mega or Google)
                product.save()
                # os.remove(file_path)
                params = {
                    'cool_mess': 'Product successfully added',
                }
            except Exception as e:
                params = {
                    'error': 'Failed to add product',
                }
    return render(request, 'add_product.html', params)


def product(request):
    name = request.path_info.strip('/')
    product = Product.objects.get(title=name)
    if request.method == 'POST':
        name_of_user = request.POST['name_of_user']
        address = request.POST['address']
        phone = request.POST['phone']
        count = request.POST['quantity']
        if product.count < int(count):
            error = 'Not enough products in the storage'
            return render(request, 'product.html', {'error': error, 'product': product, 'auth': request.session['auth']})
        else:
            order = Order.objects.create(title=name, phone=phone, name_of_user=name_of_user, count=count, address=address, district=2)
            order.save()
            Product.objects.filter(title=name).update(count=product.count - int(count))
            return redirect('base')
        product = Product.objects.get(title=name)
    try:
        return render(request, 'product.html', {'product': product, 'auth': request.session['auth']})
    except Exception as e:
        return redirect('base')


def buy_product(product, count, name_of_user, address):
    pass
