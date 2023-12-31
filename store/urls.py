from django.urls import path
from .views import store, cart, checkout, updateItem, processOrder, sendmail

urlpatterns = [
    path('', store, name="store"),
    path('cart', cart, name="cart"),
    path('checkout', checkout, name="checkout"),
    path('update_item', updateItem, name="updateitem"),
    path('process_order', processOrder, name="process_order"),
    path('sendmail', sendmail, name="sendmail"),
]
