from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from User.forms import UserLoginForm,UserRegisterForm,Personal_info_form
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import PersonalInfo
from Product.models import Order,ShippingAddress
from .send_email_tool import send_email_code


def user_login(request):
    """this function is used for user log in"""
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    context = {
        'cartItems': cartItems, }
    if request.method == 'POST':
        user_login_form =UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            username = request.POST.get("username")
            print(username)
            password = request.POST.get("password")
            print(password)
            user = authenticate(username=username, password=password)  # 只是验证功能，还没有登录
            if user:
                login(request,user)
                return HttpResponse("yeah yeah yeah!!!!!!")
            else:
                return HttpResponse("account or password is wrong, please enter again~")
        else:
            return HttpResponse("something wrong")

    return render(request, 'User/login.html', context)

def logout_view(request):
    """user log out"""
    logout(request)
    return HttpResponseRedirect(reverse('Product:home'))


def register(request):
    """for new user register. if register successfully, it will log in automatically."""
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    # judge the number of cart
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            new_user.save()
            authenticate_user = authenticate(username=new_user.username, password=request.POST['password'])
            login(request, authenticate_user)
            email = request.POST['email']
            send_email_code(email, 1)
            return HttpResponseRedirect(reverse('Product:home'))
    context = {'form': form,
               'cartItems': cartItems,}
    return render(request, 'User/register.html', context)


def personal_info(request, userid):
    """show the personal Info and past address"""
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
    my_address = ShippingAddress.objects.filter(customer_id=request.user).order_by('-date_added')

    user_info = User.objects.get(id=userid)
    if PersonalInfo.objects.filter(user_id=userid).exists():
        profile = PersonalInfo.objects.get(user_id=userid)
    else:
        profile = PersonalInfo.objects.create(user_id = user_info)
    if request.method == 'POST':
        data = request.POST
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        gender = data.get("gender")
        address = data.get("address")
        city = data.get("city")
        state = data.get("state")
        zipcode = data.get("zipcode")
        country = data.get("country")

        profile.firstname = firstname
        profile.lastname = lastname
        profile.gender = gender
        profile.address = address
        profile.city = city
        profile.state =state
        profile.zipcode = zipcode
        profile.country = country
        profile.save()
        return HttpResponseRedirect(reverse("User:personal_info", args=[userid]))
    elif request.method == 'GET':
        personal_form = Personal_info_form()
        context = {'profile_form': personal_form,
                   'profile':profile,
                   'cartItems': cartItems,
                   'shippingaddress':my_address,
                   }
        return render(request, 'User/Personal_Info.html', context)
