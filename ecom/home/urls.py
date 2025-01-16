from django.urls import path
from home.views import index, search_page

urlpatterns = [
    path('', index, name='Home'),
    path('search/', search_page, name='search'),
]
