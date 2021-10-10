from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability
from django.utils.safestring import mark_safe
from embed_video.admin import AdminVideoMixin


class ProductAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = (
        'title', 'image_data', 'publishDate', 'category', 'format', 'rating', 'price_dollar', 'availability',
        'created_time')

    # fields = ('title', 'image', 'publishDate', "category", 'format', 'rating', 'price', 'availability',)

    def price_dollar(self, obj):
        return mark_safe("$" + str(obj.price))

    def image_data(self, obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.image.url)

    image_data.short_description = u'image desc'
    price_dollar.short_description = u'price'


admin.site.site_header = "Aoligei E-Commerce Administration"
admin.site.site_title = "Aoligei E-Commerce Administration"
admin.site.index_title = "Aoligei E-Commerce Administration"

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating)
admin.site.register(Format)
admin.site.register(Availability)
