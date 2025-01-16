from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone


from .models import Profile, Cart, CartItem, Order
from products.models import Coupon

# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if  not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid email or password')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, 'Email already registered')
            return HttpResponseRedirect(request.path_info)
        
        
        user_obj = User.objects.create_user(first_name= first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'Email has been sent to your mailbox')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')

def activate_email (request, email_token):
    try:
        user= Profile.objects.get()
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid token")
    
def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def profile_page(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_image = request.FILES.get('profile_image')

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile = user.profile
            if profile_image:
                profile.profile_image = profile_image
            profile.save()
            return redirect('profile')
        user_orders = Order.objects.filter(user=user).order_by('-created_at')

        return render(request, 'accounts/profile.html', {'user': request.user, 'orders': user_orders})
    else:
        return redirect('/account/login')
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        retype_password = request.POST.get('retype_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('profile')

        if new_password != retype_password:
            messages.error(request, "New password and Retype password do not match.")
            return redirect('profile')

        request.user.set_password(new_password)
        request.user.save()

        # Keep the user logged in after changing the password
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully!")
        return redirect('profile')

    return redirect('profile') 

def cart(request):
    if not request.user.is_authenticated:
         return redirect('/account/login')
    else:

        cart = Cart.objects.filter(is_paid=False, user=request.user).first()
        total_price = 0
        sub_total_price = 0
        
        if cart:
            cart_items = cart.get_cart_items()
            total_price = cart.get_cart_total()
        else:
            cart_items = []
        if request.method == 'POST':
            form_type = request.POST.get('form_type')
            if form_type == 'quantity_update':
                quantity = request.POST.get('quantity')
                cart_item = request.POST.get('cart_item')
                cart_item_obj = CartItem.objects.filter(cart=cart, uid=cart_item)
                cart_item_obj.update(quantity=quantity)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            if form_type == 'coupon':
                coupon = request.POST.get('coupon')
                coupon_obj= Coupon.objects.filter(coupon_code__icontains=coupon)
            
            if not coupon_obj:
                messages.warning(request, "Invalid coupon code")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if cart.coupon:
                messages.warning(request, "Coupon already applied")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if coupon_obj[0].is_expired:
                messages.warning(request, "Coupon expired")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if coupon_obj[0].minimum_amount > cart.get_cart_total():
                amount_needed = coupon_obj[0].minimum_amount - cart.get_cart_total()
                messages.warning(request, f"You need to spend {amount_needed} more to apply this coupon.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            cart.coupon = coupon_obj[0]
            cart.save()
            messages.success(request, "Coupon applied")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        if cart.coupon:
            sub_total_price = total_price + cart.coupon.discount_price if cart.coupon else total_price
        context = {'cart_items': cart_items, 'total_price': total_price, 'cart':cart, 'sub_total_price': sub_total_price}
        return render(request, 'accounts/cart.html', context= context)
    
    

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItem.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    if cart.coupon:
        cart.coupon = None
        cart.save()
        messages.success(request, "Coupon removed")
        
        return HttpResponseRedirect('/account/cart')
    else:
        messages.warning(request, "No coupon applied")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    if not request.user.is_authenticated:
         return redirect('/account/login')
    else:
        cart = Cart.objects.filter(is_paid=False, user=request.user).first()
        total_price = 0
        sub_total_price= 0

        if cart:
            cart_items = cart.get_cart_items()
            total_price = cart.get_cart_total()
            sub_total_price = total_price + cart.coupon.discount_price if cart.coupon else total_price
        else:
            cart_items = []
        
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('city')
            payment_method = request.POST.get('payment_method')

            print(first_name, last_name, email, phone, address, state, city, payment_method)
            
            if not all([first_name, last_name, email, phone, address, state, city, payment_method]):
                messages.warning(request, "Please fill out all required fields.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if  not cart or not cart.cart_items.exists():
                messages.error(request, "Your cart is empty.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            order = Order.objects.create(user=request.user,
                                            cart=cart, 
                                            order_date=timezone.now(), 
                                            status="pending",
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            email=email, 
                                            phone=phone, 
                                            address=address, 
                                            state=state, 
                                            city=city, 
                                            payment_method=payment_method,
                                            total_price=total_price)
            for item in cart.cart_items.all(): 
                order.cart_items.add(item)
            order.save()
            cart.is_paid=True
            cart.save()
            return render(request, 'accounts/order_success.html', {'order': order})
        
        return render(request, 'accounts/checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'cart':cart, 'sub_total_price': sub_total_price})