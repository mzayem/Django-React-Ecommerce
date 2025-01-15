
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_email
from products.models import Product, ColorVariant, SizeVariant
from products.models import Coupon


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()
    
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    coupon= models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    

    def get_cart_items(self):
        # Return all cart items for the current cart
        return self.cart_items.all()
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total_price = 0  # Initialize total price

        for cart_item in cart_items:
            product_price = cart_item.get_product_price()
            total_price += product_price  # Add the product price to total

        if self.coupon:
            return total_price - self.coupon.discount_price

        return total_price


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    colorVariant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    sizeVariant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = self.product.price if self.product else 0
        if self.colorVariant:
            price += self.colorVariant.price if self.colorVariant else 0
        if self.sizeVariant:
            price += self.sizeVariant.price if self.sizeVariant else 0
        return price * self.quantity




@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token= str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
   
    except Exception as e:
        print(e)

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default="pending")
    first_name = models.CharField(max_length=100, default="Delivery First Name")
    last_name = models.CharField(max_length=100, default="Delivery Last Name")
    email = models.CharField(max_length=100, default="Delivery Email")
    phone = models.CharField(max_length=100, default="Delivery Phone")
    address = models.CharField(max_length=100, default="Delivery Address")
    state = models.CharField(max_length=100, default="Delivery State")
    city = models.CharField(max_length=100, default="Delivery City")
    state = models.CharField(max_length=100, default="Delivery State")
    payment_method = models.CharField(max_length=100, default="cash on Delivery")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cart_items = models.ManyToManyField(CartItem, related_name="orders")

    def get_order_items(self):
        # Return all cart items for the current cart
        return self.cart.cart_items.all()
    


