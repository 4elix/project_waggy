from django import template
from payment.models import SaveOrderProduct

register = template.Library()


@register.simple_tag()
def convert_in_str(obj):
    return str(obj)


@register.simple_tag()
def get_save_product(pk):
    try:
        return SaveOrderProduct.objects.get(order_id=pk)
    except:
        pass
