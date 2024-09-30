import stripe
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .models import Customer, Order, CartProduct, SaveOrder, SaveOrderProduct
from .utils import CartForAuthenticated, get_cart_data
from .forms import CustomerForm, ShippingForm


# Create your views here.
def cart_view(request):
    cart_info = get_cart_data(request)

    context = {
        'title': 'Моя корзина',
        'order': cart_info['order'],
        'products': cart_info['products']
    }
    return render(request, 'payment/cart.html', context)


def add_product_in_cart(request, product_id, action, color=None, size=None, quantity=1):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticated(request, product_id, quantity, action, color, size)
        return redirect(request.META.get('HTTP_REFERER', 'index_path'))
    else:
        return redirect(request.META.get('HTTP_REFERER', 'index_path'))


def delete_product_cart(request, order_id, product_id, quantity, color, size, added_at):
    if color == 'None' and size == 'None':
        color = None
        size = None

    order = CartProduct.objects.get(order_id=order_id, product_id=product_id, quantity=quantity, color=color, size=size,
                                    added_at=added_at)
    order.delete()
    return redirect('cart_path')


def checkout_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)
        context = {
            'title': 'Оформления заказа',
            'order': cart_info['order'],
            'products': cart_info['products'],
            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm()
        }
        return render(request, 'payment/checkout.html', context)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticated(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data.get('first_name')
            customer.last_name = customer_form.cleaned_data.get('last_name')
            customer.phone = customer_form.cleaned_data.get('phone')
            customer.email = customer_form.cleaned_data.get('email')
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.customer = Customer.objects.get(user=request.user)
            shipping.order = cart_info['order']
            shipping.save()

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Тестовая оплата на сайте waggy !!!!'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success_path')),
            cancel_url=request.build_absolute_uri(reverse('checkout_path'))
        )

        return redirect(session.url, 303)


def success_view(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticated(request)
        cart_info = user_cart.get_cart_info()
        order = cart_info['order']

        order.is_completed = True
        order.save()

        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price)
        order_save.save()

        order_products = order.cartproduct_set.all()
        for item in order_products:
            save_order_product = SaveOrderProduct(
                order_id=order_save.pk,
                product=item.product.title,
                quantity=item.quantity,
                product_price=item.product.price,
                color=item.color,
                size=item.size,
                final_price=item.get_total_price
            )
            save_order_product.save()

        user_cart.clear_cart()
        return render(request, 'payment/success.html', context={'title': 'Спасибо'})


def list_save_product(request):
    customer = Customer.objects.get(user=request.user)
    order = SaveOrder.objects.filter(customer=customer)

    context = {
        'title': 'История покупок',
        'order': order
    }
    return render(request, 'payment/list_save_products.html', context)
