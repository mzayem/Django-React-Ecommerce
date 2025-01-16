from django.shortcuts import render
from products.models import Product

def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'home/index.html', context)


def search_page(request):
    query = request.GET.get('query', '')
    
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()  
    
    return render(request, 'home/search_page.html', {'products': products})
