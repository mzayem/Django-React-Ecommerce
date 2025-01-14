from django.shortcuts import render
from products.models import Product
from accounts.models import Cart, CartItem
from django.http import HttpResponseRedirect

# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}

        size = request.GET.get('size')
        color = request.GET.get('color')
        context['selected_size'] = product.size_variant.first().size_name
        context['selected_color'] = product.color_variant.first().color_name
        
        if size or color:
            if size:
                context['selected_size'] = size
           
            if color:
                context['selected_color'] = color

           
            price = product.get_product_price_by_variant(size, color)
            context['updated_price'] = price

            price = product.get_product_price_by_variant(size, color)
            context['updated_price'] = price
            

        return render(request, 'product/product.html', context=context)
    except Exception as e:
        print(e)

def add_to_cart(request, uid):
    size = request.GET.get('size')
    color = request.GET.get('color')

    try:
        if request.user.is_authenticated:
            product = Product.objects.get(uid=uid)
            user = request.user
            cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        # Create CartItem without 'size' and 'color' arguments
            cart_item = CartItem(cart=cart, product=product)
            if size:
                size_variant = product.size_variant.get(size_name=size)
                cart_item.sizeVariant = size_variant

        
            if color:
                color_variant = product.color_variant.get(color_name=color)  # Corrected to color_name
                cart_item.colorVariant = color_variant


            cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else: 
            return HttpResponseRedirect('/account/login')
        
    except Product.DoesNotExist:
        return HttpResponseRedirect('/')  # Redirect to home or show error if product is not found
    
    

def buy_now(request, uid):
    size = request.GET.get('size')
    color = request.GET.get('color')

    try:
        if request.user.is_authenticated:
            product = Product.objects.get(uid=uid)
            user = request.user
            cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        # Create CartItem without 'size' and 'color' arguments
            cart_item = CartItem(cart=cart, product=product)
            if size:
                size_variant = product.size_variant.get(size_name=size)
                cart_item.sizeVariant = size_variant

        
            if color:
                color_variant = product.color_variant.get(color_name=color)  # Corrected to color_name
                cart_item.colorVariant = color_variant


            cart_item.save()
            return HttpResponseRedirect('/account/cart')

        else: 
            return HttpResponseRedirect('/account/login')
        
    except Product.DoesNotExist:
        return HttpResponseRedirect('/')  # Redirect to home or show error if product is not found
