from django.urls import path, include, re_path
from Product import views
from django.views.static import serve
from django.conf import  settings

app_name = 'Product'

urlpatterns = [
    path('', views.home, name='home'),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
