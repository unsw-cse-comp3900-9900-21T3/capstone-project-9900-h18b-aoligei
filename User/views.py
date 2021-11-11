from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from User.forms import UserLoginForm,UserRegisterForm,Personal_info_form
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import PersonalInfo
from Product.models import Order,ShippingAddress



from django.core.mail import send_mail
from .send_email_tool import send_email_code
from User.models import EmailVertifyCode


# Create your views here. 操作数据库 resful

def user_login(request):
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    context = {
        'cartItems': cartItems, }

    if request.method == 'POST':
        user_login_form =UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # data = user_login_form.cleaned_data
            # user = authenticate(username = data['username'],password = data['password'])
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
    """用户登出"""
    logout(request)
    return HttpResponseRedirect(reverse('Product:home'))


def register(request):

    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    if request.method != 'POST':
        # 显示空的注册表单
        form = UserRegisterForm()
    else:
        # 处理填写好的表单
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("yeah")
            new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])

            new_user.save()
            # 让用户自动登陆，再重定向 到主页位置
            print(new_user.password)
            print(request.POST['password'])
            authenticate_user = authenticate(username=new_user.username, password=request.POST['password'])

            print(111)
            login(request, authenticate_user)
            print("2222")
            email = request.POST['email']

            send_email_code(email, 1)

            return HttpResponseRedirect(reverse('Product:home'))

    context = {'form': form,
               'cartItems': cartItems,}
    return render(request, 'User/register.html', context)


def personal_info(request, userid):
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
    print("1234567890")
    if PersonalInfo.objects.filter(user_id=userid).exists():
        profile = PersonalInfo.objects.get(user_id=userid)
    else:
        print(44444444444)
        profile = PersonalInfo.objects.create(user_id = user_info)

    print(333333)
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
        print("saved")
            # 和查看用户信息同理，每个用户都有自己的路由，修改后，重定向到新的路由
            # 因为该路由由用户名决定
        # return render(request, 'User/register.html', '')
        return HttpResponseRedirect(reverse("User:personal_info", args=[userid]))
    elif request.method == 'GET':
        personal_form = Personal_info_form()
        context = {'profile_form': personal_form,
                   'profile':profile,
                   'cartItems': cartItems,
                   'shippingaddress':my_address,
                   }
        return render(request, 'User/Personal_Info.html', context)



def activate(request,code):
    # if code:
    #     email_vertification_list = EmailVertifyCode.objects.filters(code = code)
    #     if email_vertification_list:
    #         email_ver = email_vertification_list[0]
    #         email = email_ver.email
    #         user = User()
    #
    pass
