from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index_path'),
    path('product/<slug:slug>/', views.single_product, name='product_path'),
    path('login/', views.login_view, name='login_path'),
    path('register/', views.register_view, name='register_path'),
    path('logout/', views.logout_view, name='logout_path'),
    path('account/', views.account_view, name='account_path'),
    path('favorite/<int:product_pk>/', views.favorite_activate, name='favorite_activate'),
    path('favorite/', views.favorite_view, name='favorite_path'),
    path('shop/', views.shop_view, name='shop_path')
]
