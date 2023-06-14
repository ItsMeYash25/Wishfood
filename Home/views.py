from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from .models.tablereserve import TableReserve
from .models.contactus import Contact
from datetime import datetime
from django.contrib import messages
from store.models.orders import *
from store.models.product import Product

def index(request):
    #cart item
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']
    data = {}
    data['cartItem'] = cartItem

    name = auth.get_user(request)
    if request.method == "POST":
        if request.user.is_authenticated:
            date = request.POST.get('date')
            time = request.POST.get('time')
            member = request.POST.get('member')
            trs = TableReserve(username=name, date=date, time=time, member=member)
            trs.save()
            messages.success(request, "Your Table reserved successfully.")
        else:
            messages.warning(request, "You need to login first!!")
            return redirect('Account/login')
    return render(request, 'index.html', data)

def contact(request):
    #cart item
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']
    data = {}
    data['cartItem'] = cartItem

    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('email')
        msg = request.POST.get('message')
        cntus = Contact(name=name, email=email, desc=msg, date=datetime.today())
        cntus.save()
        messages.success(request, "Your message has been sent!!")
    return render(request, 'contactus.html', data)

# def error_404_view(request, exception):
#     return render(request,'404.html')
