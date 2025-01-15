from django.contrib import admin
from django.urls import path
from accounts.views import profile_page, login_page, register_page, activate_email, logout_user, cart, remove_cart, change_password, remove_coupon, checkout
from products.views import add_to_cart, buy_now

urlpatterns = [
    path('', profile_page, name='profile'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_user, name='logout'),
     path('change_password/', change_password, name='change_password'),
    path('activate/<email_token>/', activate_email, name='activate'),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<uid>', add_to_cart, name="add_to_cart"),
    path('buy_now/<uid>', buy_now, name="buy_now"),
    path('remove_cart/<cart_item_uid>', remove_cart, name="remove_cart"),
    path('remove_coupon/<cart_id>', remove_coupon, name="remove_coupon"),
    path('checkout/', checkout, name="checkout")
]
