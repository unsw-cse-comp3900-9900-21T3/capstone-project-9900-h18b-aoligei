from django.urls import path, include, re_path
from Product import views
from django.views.static import serve
from django.conf import settings
from .views import *

app_name = 'Product'

urlpatterns = [
    path('', views.home, name='home'),

    path(r'product_id=<int:product_id>', getProduct, name='getProduct'),

    path('item/', views.product_item, name='product_item'),

    path('search/', views.search, name='search'),

    path('products/dashboard/', views.dashboard, name='dashboard'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
