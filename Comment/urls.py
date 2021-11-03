from django.urls import path, include,re_path
from django.conf.urls import url
from Comment import views
from django.views.static import serve
from django.conf import settings
app_name = 'Comment'

urlpatterns = [

    path(r'post_comment/<int:product_id>', views.post_comment, name='post_comment'),
    path(r'post_comment/<int:product_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
    path(r'edit_comment/<int:comment_id>',views.edit_comment,name='edit_comment'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
