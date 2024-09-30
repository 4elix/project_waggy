from django import template
from pages.models import ProductFavorite, Category, Tag, Brand
from payment.utils import get_cart_data

register = template.Library()


@register.simple_tag()
def status_favorite(auth_id, product_id):
    return ProductFavorite.objects.filter(auth_id=auth_id, product_id=product_id)


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_brands():
    return Brand.objects.all()


@register.simple_tag()
def get_tags():
    return Tag.objects.all()


@register.simple_tag()
def query_transform(request, key, value):
    updated = request.GET.copy()
    updated[key] = value
    return updated.urlencode()


@register.simple_tag()
def get_sorters():
    return [
        ('title', 'Name (A-Z)'),
        ('-title', 'Name (Z-A)'),
        ('price', 'Price (Low-High)'),
        ('-price', 'Name (High-Low)'),
    ]


@register.simple_tag()
def get_cart_products(request):
    cart_info = get_cart_data(request)
    return cart_info['products']
