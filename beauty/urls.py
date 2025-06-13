from django.contrib.messages.api import success
from django.urls import path, include
from . import views
from . import utils
from django.contrib.auth import views as auth_views, logout
from .views import login_registration, user_login, register

urlpatterns = [

    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('login_registration/', views.login_registration, name='login_registration'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('update-cart/', utils.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', utils.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', utils.add_to_cart, name='add_to_cart'),
    path('cart/', utils.cart_view, name='cart_view'),
    path('update-cart/', utils.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', utils.remove_from_cart, name='remove_from_cart'),
    path('cart-count/', utils.get_cart_count, name='cart_count'),
    path('checkout/', utils.checkout_view, name='checkout'),
    path('confirm-order/', utils.confirm_order_views, name='confirm_order'),
    path('order-success/', utils.order_success_view, name='order_success'),
	path('sovunlar/', views.sovunlar_product_list,  name='sovunlar_product_list')

]

