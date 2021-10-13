from django.shortcuts import render
from .models import Product, Category, Rating, Format, Availability, Score
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Avg
import markdown


def home(request):
    '''new_products = Product.objects.all().order_by("-created_time")[:4]
    context = {"new_products": new_products}
    return render(request, 'home.html', context)'''
    if request.method == "GET":
        product_new_release = Product.objects.filter().order_by("-publishDate")[:4]
        # product_spotlight=Product.objects.group_by('product').annotate(title_avg=Avg('title')).order_by('-title_avg')[:4]
        product_spotlight = Score.objects.values("product_id").annotate(avg=Avg("title")).values("product_id",
                                                                                                 "avg").order_by(
            '-avg')[:4]
        product_all = Product.objects.all()
        kwarg = {
            "product_new_release": product_new_release,
            "product_spotlight": product_spotlight,
            "product_all": product_all,
        }
    return render(request, 'home.html', kwarg)


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


def getProduct(request, product_id):
    product = Product.objects.get(id=product_id)

    score = Score.objects.filter(product=product_id).aggregate(Avg('title'))
    score = score['title__avg']

    product.description = markdown.markdown(product.description,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])

    product.details = markdown.markdown(product.details,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                        ])
    kwarg = {
        "product": product,
        "score": score,
    }
    return render(request, 'Product/item_info.html', kwarg)


def dashboard(request):
    user_count = User.objects.count()
    product_count = Product.objects.count()
    context = {'user_count': user_count, 'product_count': product_count}
    return render(request, 'Product/dashboard.html', context)
