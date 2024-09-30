from django.db import models
from django.contrib.auth.models import User

from pages.models import Product


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)

    def __str__(self):
        return f'{self.first_name} --- {self.last_name}'


class ShippingAddress(models.Model):
    name_company = models.CharField(max_length=250, blank=True, null=True)
    city_or_region = models.ForeignKey('CityOrRegion', on_delete=models.CASCADE)
    address_part_one = models.CharField(max_length=250)
    address_part_two = models.CharField(max_length=250)
    town_city = models.CharField(max_length=250)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=250)
    order_notes = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.address_part_one} --- {self.address_part_two}'


class CityOrRegion(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)

    def __str__(self):
        return f'№ {self.pk}'

    @property
    def get_cart_total_quantity(self):
        cart_product = self.cartproduct_set.all()
        total_quantity = sum([product.quantity for product in cart_product])
        return total_quantity

    @property
    def get_cart_total_price(self):
        cart_product = self.cartproduct_set.all()
        total_price = sum([product.get_total_price for product in cart_product])
        return total_price


class CartProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        if self.product.discount <= 0:
            total_price = float(self.product.price) * self.quantity
        else:
            total_price = float(self.product.price) - float(self.product.price) * self.product.discount / 100

        return total_price


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'Номер заказа №{self.pk}'


class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, null=True, related_name='order_products')
    product = models.CharField(max_length=250)
    quantity = models.IntegerField(default=0)
    product_price = models.FloatField()
    final_price = models.FloatField()
    color = models.CharField(max_length=250, null=True, blank=True)
    size = models.CharField(max_length=250, null=True, blank=True)
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product
