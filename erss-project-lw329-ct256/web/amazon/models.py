import uuid
import random
from django.db import models
from django.contrib.auth.models import User

def UUID64():
    return (uuid.uuid1().int) >> 66

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    ups_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, null = True, unique=True)
    address = models.CharField(max_length=30, null = True)
    state = models.CharField(max_length=30, null = True)
    country = models.CharField(max_length=30, null = True)

class Warehouse(models.Model):
    x = models.IntegerField(null = False)
    y = models.IntegerField(null = False)

class Order(models.Model):
    initialized = "initialized"
    purchasing = "purchasing"
    packing = "packing"
    packed = "packed"
    loading = "loading"
    loaded = "loaded"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"
    status_choices = (
        (initialized, "initialized"),
        (purchasing, "purchasing"),
        (packing, "packing"),
        (packed, "packed"),
        (loading, "loading"),
        (loaded, "loaded"),
        (delivering, "delivering"),
        (delivered, "delivered"),
        (cancelled, "cancelled")
    )

    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null = False, db_column="user_id")
    status = models.CharField(max_length=15, choices=status_choices, default="initialized")
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null = True, db_column='warehouse_id')
    ups_name = models.CharField(max_length=20, null = True)
    shipid_or_packageid = models.BigIntegerField(default=UUID64, null=False)
    truck_id = models.IntegerField(null = True)
    dest_x = models.IntegerField(default = 1, null = False)
    dest_y = models.IntegerField(default = 2, null = False)
    created_at = models.DateTimeField(null = False, auto_now = True)
    packed_at = models.DateTimeField(null = True)
    loaded_at = models.DateTimeField(null = True)
    delivered_at = models.DateTimeField(null = True)

class Category(models.Model):
    cat_name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=True)

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=50, null=True)
    photo = models.ImageField(upload_to='.')
    category_id = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, db_column='category_id')

class orderProduct(models.Model):
    order_id = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, db_column='order_id')
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, db_column='product_id')
    count = models.IntegerField(null=False)

class Cart(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null = False, db_column='user_id')

class cartProduct(models.Model):
    cart_id = models.ForeignKey(Cart, null=False, on_delete=models.CASCADE, db_column='cart_id')
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, db_column='product_id')
    count = models.IntegerField(default=1, null=False)