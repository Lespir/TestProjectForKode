from django.contrib import admin
from .models import Manager, Product, Order, Courier


admin.site.register(Manager)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Courier)
# Register your models here.
