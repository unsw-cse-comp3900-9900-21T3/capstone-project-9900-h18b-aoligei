from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserLoginForm

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# Create your views here. 操作数据库 resful

def user_login(request):
    if request.method == 'POST':
        user_login_form =UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username = data['username'],password = data['password'])
            if user:
                login(request,user)
                return HttpResponse("yeah yeah yeah!!!!!!")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    else:
        return HttpResponse("请使用GET或POST请求数据")

def logout_view(request):
    """用户登出"""
    logout(request)
    return HttpResponseRedirect(reverse('Product:home'))


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登陆，再重定向 到主页位置
            authenticate_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('Product:home'))

    context = {'form': form}
    return render(request, 'User/register.html', context)