from django.shortcuts import redirect
from django.contrib import messages

from .models import Product, Order, Customer, CartProduct


class CartForAuthenticated:
    def __init__(self, request, product_id=None, quantity=1, action=None, color=None, size=None):
        self.user = request.user
        self.request = request

        if product_id and action:
            self.add_or_delete(product_id, action, quantity, color, size)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        cart_product = order.cartproduct_set.all()

        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity

        return {
            'order': order,
            'products': cart_product,
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity
        }

    def add_or_delete(self, product_id, action, quantity, color, size):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)

        cart_product, created = CartProduct.objects.get_or_create(order=order, product=product,
                                                                  color=color, size=size)

        if action == 'add' and product.in_stock > 0:
            cart_product.quantity += int(quantity)
            product.in_stock -= int(quantity)
        else:
            cart_product.quantity -= int(quantity)
            product.in_stock += int(quantity)

        product.save()
        cart_product.save()

        if cart_product.quantity <= 0:
            cart_product.delete()

    def clear_cart(self):
        order = self.get_cart_info()['order']
        order_product = order.cartproduct_set.all()
        for product in order_product:
            product.delete()

        order.save()


def get_cart_data(request):
    cart = CartForAuthenticated(request)
    cart_info = cart.get_cart_info()

    return {
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity']
    }
