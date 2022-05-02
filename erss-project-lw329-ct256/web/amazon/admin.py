from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Warehouse)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(orderProduct)
admin.site.register(Cart)
admin.site.register(cartProduct)