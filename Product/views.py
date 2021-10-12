from django.shortcuts import render
from .models import Product, Category, Rating, Format, Availability
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def home(request):
    new_products = Product.objects.all().order_by("-created_time")[:4]
    context = {"new_products": new_products}
    return render(request, 'home.html', context)


def search(request):
    products = Product.objects.all()

    # search code
    item_name = request.GET.get("item_name")
    if item_name != '' and item_name is not None:
        products = products.filter(title__icontains=item_name) | \
                   products.filter(price__icontains=item_name) | \
                   products.filter(format__title__icontains=item_name) | \
                   products.filter(category__title__icontains=item_name) | \
                   products.filter(rating__title__icontains=item_name) | \
                   products.filter(availability__title__icontains=item_name)

    # paginator code
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    products = paginator.get_page(page)


    context = {'products': products}
    return render(request, 'Product/search.html', context)


def product_item(request):
    return render(request, 'Product/item_info.html')


def dashboard(request):
    user_count = User.objects.count()
    product_count = Product.objects.count()
    context = {'user_count': user_count, 'product_count': product_count}
    return render(request, 'Product/dashboard.html', context)
