from django.contrib import admin
from django.urls import path
from accounts.views import login_page, register_page, activate_email, cart
from products.views import add_to_cart

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('activate/<email_token>/', activate_email, name='activate'),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<uid>', add_to_cart, name="add_to_cart")
]
