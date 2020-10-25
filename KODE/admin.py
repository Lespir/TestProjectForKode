from django.contrib import admin
from .models import KodeUser, Product, Order


admin.site.register(KodeUser)
admin.site.register(Product)
admin.site.register(Order)
# Register your models here.
