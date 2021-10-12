from django.shortcuts import render
from .models import Product, Category, Rating, Format, Availability
from django.contrib.auth.models import User


def home(request):
    new_products = Product.objects.all().order_by("-created_time")[:4]
    context = {"new_products": new_products}
    return render(request, 'home.html', context)


def dashboard(request):
    user_count = User.objects.count()
    product_count = Product.objects.count()
    context = {'user_count': user_count, 'product_count': product_count}
    return render(request, 'Product/dashboard.html', context)
