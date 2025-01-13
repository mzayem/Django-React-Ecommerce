from django.shortcuts import render
from products.models import Product

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
            print(price)

            price = product.get_product_price_by_variant(size, color)
            context['updated_price'] = price
            

        return render(request, 'product/product.html', context=context)
    except Exception as e:
        print(e)
