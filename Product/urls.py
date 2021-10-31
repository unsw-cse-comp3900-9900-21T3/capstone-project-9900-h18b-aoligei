from django.urls import path, include, re_path
from Product import views
from django.views.static import serve
from django.conf import settings
from .views import *

app_name = 'Product'

urlpatterns = [
    path('', views.home, name='home'),

    path(r'product_id=<int:product_id>', getProduct, name='getProduct'),

    path('search/', views.search, name='search'),

    path('category_list/', views.CategoryIndexView.as_view(), name='category_list'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order', views.processOder, name='process_order'),

    path('products/dashboard/', views.dashboard, name='dashboard'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
