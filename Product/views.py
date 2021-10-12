from django.shortcuts import render
from .models import Product, Category, Rating, Format, Availability
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

def product_item(request):
    return render(request, 'Product/item_info.html')

def dashboard(request):
    user_count = User.objects.count()
    product_count = Product.objects.count()

    context = {'user_count': user_count, 'product_count': product_count}
    return render(request, 'Product/dashboard.html', context)
