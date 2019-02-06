from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from .models import *


def index(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'image_url': product.image.url,
            'title': product.title,
            'price': product.price,
            'currency': product.currency.code,
            'description': product.description
        })

    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = None

    context = {
        'products': data,
        'username': username
    }

    return render(request, 'index.html', context)


def log_out(request):
    logout(request)
    return redirect('index')


def log_in(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return render(request, 'login.html')

    login(request, user)
    return redirect('index')


def register(request):
    user: User = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username, password=password)
        user.save()
    except Exception as exc:
        print(exc, type(exc))
        return render(request, 'register.html')

    login(request, user)
    return redirect('index')


def product(request, id):
    product = Product.objects.get(id=id)

    user: User = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = None

    context = {
        'product':
            {
                'image_url': product.image.url,
                'title': product.title,
                'price': product.price,
                'currency': product.currency.code,
                'description': product.description,

            },
        'username': username
        }
    login(request, user)
    return render(request, 'product.html', context)


def order(request):
    if request.method == 'GET':
        return render(request, 'order.html')

    first_name = request.POST['first_name']
    second_name = request.POST['second_name']
    country = request.POST['country']
    city = request.POST['city']
    street = request.POST['street']
    building = request.POST['building']
    flat = request.POST['flat']
    item = request.POST['item']

    or_der = Order.objects.create(first_name=first_name, second_name=second_name, country=country, city=city, street=street, building=int(request.POST['building']), flat=int(request.POST['flat']), item=item)
    or_der.save()

    #return render(request, 'index.html')
    return redirect('index')
