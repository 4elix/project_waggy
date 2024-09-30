from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart_path'),
    path('add/cart/<int:product_id>/<str:action>/<str:color>/<str:size>/<int:quantity>/', views.add_product_in_cart,
         name='add_product_cart'),
    path('delete/cart/<int:order_id>/<int:product_id>/<int:quantity>/<str:color>/<str:size>/<str:added_at>/',
         views.delete_product_cart, name='delete_product_cart'),

    # пути для прибавления продукта в корзину
    path('product/plus/cart/<int:product_id>/<str:action>/', views.add_product_in_cart, name='plus_v1'),
    path('product/plus/cart/<int:product_id>/<str:action>/<str:color>/<str:size>/<int:quantity>/',
         views.add_product_in_cart, name='plus_v2'),

    # пути для уменьшения продукта в корзину
    path('product/plus/cart/<int:product_id>/<str:action>/', views.add_product_in_cart, name='minus_v1'),
    path('product/plus/cart/<int:product_id>/<str:action>/<str:color>/<str:size>/<int:quantity>/',
         views.add_product_in_cart, name='minus_v2'),

    path('checkout/', views.checkout_view, name='checkout_path'),
    path('pay/', views.create_checkout_session, name='pay_activate'),
    path('success/', views.success_view, name='success_path'),
    path('list/save/product/', views.list_save_product, name='list_save_product')
]