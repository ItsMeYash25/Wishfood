from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from Account.models import Customer
from .models.orders import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import datetime

# Create your views here.

#Store method
@login_required(login_url='login')
def store(request):
    product = None
    category = Category.get_all_categories()
    categoryid = request.GET.get("categories")
    if categoryid:
        product = Product.get_categories_by_id(categoryid)
    else:
        product = Product.get_all_product
    
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
    data['category'] = category
    data['products'] = product
    data['cartItem'] = cartItem
    return render(request, 'Store.html', data)

#Cart method
@login_required(login_url='login')
def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']
    
    context = {'item':items, 'order': order, 'cartItem':cartItem}
    return render(request, 'cart.html', context)


#Checkout method
@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']
    
    context = {'item':items, 'order': order, 'cartItem':cartItem}
    return render(request, 'checkout.html', context)


#UpdateItems method
@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("product Id: ",productId)
    print("Acion: ",action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Orders.objects.get_or_create(customer = customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item added', safe=False)

@login_required(login_url='login')
def processOrder(request):
    transection_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        price = float(data['total'])
        order.transaction_id = transection_id
        sendmail(request)
        if price == order.get_cart_total:
            order.complete = True
        order.save()
    else:
        print('user is not logged in')
    return JsonResponse('Payment Success..', safe=False)


#email invoice
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import auth, User
from datetime import datetime

def sendmail(request):
    name = auth.get_user(request)
    customeremail = request.user.customer.email
    dt = datetime.today()
    # print(dt)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Orders.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0}
        cartItem = order['get_cart_items']
    context = {'item':items, 'order': order, 'cartItem':cartItem, 'name':name, 'email':customeremail, 'datetime':dt,}
    template = render_to_string('extras/email.html', context)
    content = strip_tags(template)
    email = EmailMultiAlternatives(
        'Your Wishfood Order Receipt',
        content,
        settings.EMAIL_HOST_USER,
        [customeremail],
    )
    email.attach_alternative(template,"text/html")
    email.send()
    return render(request, 'index.html')