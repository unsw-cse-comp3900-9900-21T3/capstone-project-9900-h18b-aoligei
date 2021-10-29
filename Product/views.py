from django.shortcuts import render
from .models import Product, Category, Rating, Format, Availability, Score
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Avg
import markdown
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.db.models.aggregates import Count


def home(request):
    '''new_products = Product.objects.all().order_by("-created_time")[:4]
    context = {"new_products": new_products}
    return render(request, 'home.html', context)'''
    if request.method == "GET":
        product_new_release = Product.objects.filter().order_by("-publishDate")[:4]
        # product_spotlight=Product.objects.group_by('product').annotate(title_avg=Avg('title')).order_by('-title_avg')[:4]
        product_spotlight = Score.objects.values("product_id").annotate(avg=Avg("score")).values("product_id",
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
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    category_list = Category.objects.filter(status=True).values()

    context = {'products': products, 'category_list': category_list}
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


class CategoryIndexView(generic.ListView):
    model = Product
    template_name = 'Product/category.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        # category_list = Category.objects.filter(status=True).values()
        category_list = Category.objects.annotate(num_products=Count('product'))
        format_list = Format.objects.annotate(num_products=Count('product'))
        rating_list = Rating.objects.annotate(num_products=Count('product'))
        availability_list = Availability.objects.annotate(num_products=Count('product'))

        context['category_list'] = category_list
        context['format_list'] = format_list
        context['rating_list'] = rating_list
        context['availability_list'] = availability_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        self.f = self.request.GET.get("f", None)
        self.r = self.request.GET.get("r", None)
        self.a = self.request.GET.get("a", None)
        if self.c:
            category = get_object_or_404(Category, pk=self.c)
            return category.product_set.all().order_by('-publishDate')
        elif self.f:
            format = get_object_or_404(Format, pk=self.f)
            return format.product_set.all().order_by('-publishDate')
        elif self.r:
            rating = get_object_or_404(Rating, pk=self.r)
            return rating.product_set.all().order_by('-publishDate')
        elif self.a:
            availability = get_object_or_404(Availability, pk=self.a)
            return availability.product_set.all().order_by('-publishDate')
        else:
            return Product.objects.filter().order_by('-publishDate')
