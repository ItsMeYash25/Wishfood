from django.contrib import admin
from .models.tablereserve import TableReserve
from .models.contactus import Contact

# Register your models here.

admin.site.register(TableReserve)
admin.site.register(Contact)