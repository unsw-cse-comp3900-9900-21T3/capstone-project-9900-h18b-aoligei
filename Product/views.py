from django.shortcuts import render
from django.utils import timezone
from .models import Product, Category, Rating, Format, Availability, Score, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Avg
import markdown
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.db.models.aggregates import Count
from django.http import JsonResponse
import json
# import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from Comment.models import Comment
from Comment.forms import CommentForm
import datetime
from ContentBasedRecommender import get_recommendations, cosine_sim, cosine_sim2, indices, indices2
import numpy as np
from .forms import ScoreForm


def home(request):
    '''
    transmitting parameters to homepage
    '''
    kwarg = {}
    # new release 10 products in recently time
    product_new_release = Product.objects.filter().order_by("-publishDate")[:10]
    # score rantings
    product_spotlight = Score.objects.values("product_id").annotate(avg=Avg("score")).values("product_id",
                                                                                             "avg").order_by(
        '-avg')[:8]
    product_all = Product.objects.all()
    kwarg['product_new_release'] = product_new_release
    kwarg['product_spotlight'] = product_spotlight
    kwarg['product_all'] = product_all

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    kwarg['cartItems'] = cartItems
    return render(request, 'home.html', kwarg)


def search(request):
    '''
    transmitting parameters to search page
    '''
    products = Product.objects.all()
    # search code
    item_name = request.GET.get("item_name")
    if item_name != '' and item_name is not None:
        products = products.filter(title__icontains=item_name) | \
                   products.filter(title_zh__icontains=item_name) | \
                   products.filter(price__icontains=item_name) | \
                   products.filter(format__title__icontains=item_name) | \
                   products.filter(category__title__icontains=item_name) | \
                   products.filter(rating__title__icontains=item_name) | \
                   products.filter(availability__title__icontains=item_name)
    # paginator code
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    category_list = Category.objects.annotate(num_products=Count('product'))
    format_list = Format.objects.annotate(num_products=Count('product'))
    rating_list = Rating.objects.annotate(num_products=Count('product'))
    availability_list = Availability.objects.annotate(num_products=Count('product'))

    c = request.GET.get("c", None)
    f = request.GET.get("f", None)
    r = request.GET.get("r", None)
    a = request.GET.get("a", None)
    if c:
        category = get_object_or_404(Category, pk=c)
        products = category.product_set.all().order_by('-publishDate')
    elif f:
        format = get_object_or_404(Format, pk=f)
        products = format.product_set.all().order_by('-publishDate')
    elif r:
        rating = get_object_or_404(Rating, pk=r)
        products = rating.product_set.all().order_by('-publishDate')
    elif a:
        availability = get_object_or_404(Availability, pk=a)
        products = availability.product_set.all().order_by('-publishDate')

    context = {
        'products': products,
        'cartItems': cartItems,
        'category_list': category_list,
        'format_list': format_list,
        'rating_list': rating_list,
        'availability_list': availability_list,
    }

    return render(request, 'Product/search.html', context)


def getProduct(request, product_id):
    '''
    transmitting parameters to product detail page
    '''
    product = Product.objects.get(id=product_id)

    score = Score.objects.filter(product=product_id).aggregate(Avg('score'))
    score = score['score__avg']
    score = round(score, 1)

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
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    comments = Comment.objects.filter(product=product_id)
    comment_form = CommentForm()

    # based on content recommendation
    content_recommend_products = get_recommendations(str(product.title), cosine_sim2, indices2)[:5]
    crp = []
    crp_id = []
    content_recommend_products = np.array(content_recommend_products)
    for i in content_recommend_products:
        crp.append(i[6])
        crp_id.append(i[1])
    # r_products = content_recommend_products.to_html(classes = 'data', header='true')
    print(crp)

    kwarg = {
        "product": product,
        "score": score,
        'cartItems': cartItems,
        'comments': comments,
        'comment_form': comment_form,
        'content_recommend_products': crp,
        'content_recommend_products_id': crp_id,
    }

    return render(request, 'Product/item_info.html', kwarg)


def cart(request):
    '''
    transmitting parameters to shopping cart
    '''
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Product/cart.html', context)


def checkout(request):
    '''
    transmitting parameters to checkout page
    '''
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Product/checkout.html', context)


def updateItem(request):
    '''
    in the cart page, add/remover products
    '''
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    if action == 'delete':
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOder(request):
    '''
    transmitting parameters in the process of checkout
    '''
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country=data['shipping']['country'],
            )
    else:
        print("User is not logged in")

    return JsonResponse("Payment submitted ...", safe=False)


def dashboard(request):
    '''
    transmitting the related parameters
    to the dashbard page (web traffic) to the admin system
    '''
    today = datetime.datetime.now().date()
    weekdelta = datetime.datetime.now().date() - datetime.timedelta(weeks=1)
    orders = Order.objects.all()
    products = Product.objects.all()
    user_count = User.objects.count()
    total_product = Product.objects.count()
    total_customer = User.objects.filter(is_superuser=False).count()
    total_comment = Comment.objects.count()
    total_price = 0
    total_cost = 0
    for product in products:
        if product.discount_price:
            total_price += product.discount_price
        else:
            total_price += product.price
        if product.cost:
            total_cost += product.cost

    avg_price = total_price / total_product
    avg_cost = total_cost / total_product

    total_sales_quantity = sum([order.get_cart_items for order in orders])
    orders_count = orders.count()
    total_sales = sum([order.get_cart_total for order in orders])
    profit = ((total_sales - total_cost) / total_cost) * 100

    # weekly new_users
    new_users = User.objects.filter(date_joined__gte=weekdelta, date_joined__lte=today, is_superuser=False).count()
    new_products = Product.objects.filter(created_time__gte=weekdelta, created_time__lte=today).count()
    new_comments = Comment.objects.filter(created__gte=weekdelta, created__lte=today).count()

    # week sales 7 days
    now_time = datetime.datetime.now()
    # compute the days to the last sunday
    day_num = now_time.isoweekday()

    days = []
    for i in range(day_num + 1):
        day = (now_time - datetime.timedelta(days=day_num - i)).date()
        days.append(day)

    weekly_sales = []
    for i in range(len(days) - 1):
        day_orders = Order.objects.filter(date_ordered__lt=days[i + 1], date_ordered__gt=days[i], complete=True)
        print(day_orders)
        if day_orders:
            day_sales = sum([order.get_cart_total for order in day_orders])
            weekly_sales.append(day_sales)
        else:
            weekly_sales.append(0)
    today_ret_orders = Order.objects.filter(date_ordered__gt=now_time.date(), complete=True)
    if today_ret_orders:
        today_sales = sum([order.get_cart_total for order in today_ret_orders])
        weekly_sales.append(today_sales)
    else:
        weekly_sales.append(0)

    context = {
        'user_count': user_count,
        'total_product': total_product,
        'total_sales': total_sales,
        'total_sales_quantity': total_sales_quantity,
        'orders_count': orders_count,
        'total_customer': total_customer,
        'total_comment': total_comment,
        'avg_price': avg_price,
        'avg_cost': avg_cost,
        'total_cost': total_cost,
        'profit': profit,
        'new_users': new_users,
        'new_products': new_products,
        'new_comments': new_comments,
        'weekly_sales': weekly_sales,
    }
    return render(request, 'Product/dashboard.html', context)


def my_order(request):
    '''
    transmitting the parameters to the personal orders page,
    so that logined user can check their order informations
    '''
    # user = User.objects.filter(id=user_id)
    my_orders = Order.objects.filter(customer=request.user, complete=True).order_by('-date_ordered')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {
        'my_orders': my_orders,
        'cartItems':cartItems,
    }
    return render(request, 'test.html', context)


def get_orderItem(request, order_id):
    '''
        transmitting the parameters to the personal order-item page,
        user check each order information including each order item
    '''
    order = get_object_or_404(Order, id=order_id)

    if order.customer != request.user:
        raise Http404
    orderItems = order.orderitem_set.filter(order__complete=True).order_by('-date_added')
    shipping_address = order.shippingaddress_set.order_by('-date_added')

    if request.user.is_authenticated:
        customer = request.user
        order1, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order1.orderitem_set.all()
        cartItems = order1.get_cart_items
    else:
        # create empty cart for none logged in users
        items = []
        order1 = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order1['get_cart_items']

    context = {'order': order,
               'orderItems': orderItems,
               'shipping_address': shipping_address,
               'cartItems':cartItems,
               }
    return render(request, 'testOrderItem.html', context)


def putScore(request,product_id):
    '''
        user publish score in the product detail page
    '''
    product=get_object_or_404(Product, id=product_id)
    if request.method=='POST':
        sc_form=ScoreForm(request.POST)
        if sc_form.is_valid():
            sc=sc_form.save(commit=False)
            sc.product=product
            sc.user=request.user
            sc.save()
            return redirect(product)
        else:
            return render(request, "empty_content_fail.html", locals())
    else:
        sc_form=ScoreForm()
        context={
            'sc_form':sc_form,
            'product_id':product_id,
            'product':product,
        }
        return render(request, 'Product/item_info.html', context)

