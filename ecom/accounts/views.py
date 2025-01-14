from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse

from .models import Profile, Cart, CartItem

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
        
        print(email)
        
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

        return render(request, 'accounts/profile.html', {'user': request.user})
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
        
        # Use the method defined in the Cart model to get the cart items
        if cart:
            cart_items = cart.get_cart_items()
        else:
            cart_items = []
        
        # Pass the cart items to the template
        context = {'cart_items': cart_items, 'total_price': cart.get_cart_total()}
        return render(request, 'accounts/cart.html', context= context)
    
    

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItem.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
