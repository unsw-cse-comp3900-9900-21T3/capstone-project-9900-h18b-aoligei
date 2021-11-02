from django.urls import path
from django.contrib.auth.views import LoginView
from User import views

app_name = 'Users'

urlpatterns = [

    path(r'login/', LoginView.as_view(template_name='User/login.html'), name='login'),
    path(r'logout/', views.logout_view, name='logout'),
    path(r'register/', views.register, name='register'),
    path(r'activate/(\w+)',views.activate,name = 'activate'),
    path(r'personal_info/<int:userid>/', views.personal_info, name='personal_info'),


]
