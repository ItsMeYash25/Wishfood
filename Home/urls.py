from django.urls import path
from .views import index, contact

urlpatterns = [
    path('', index, name="index"),
    path('contact-us', contact, name="contact"),
]
