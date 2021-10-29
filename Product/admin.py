from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability, Score
from django.utils.safestring import mark_safe
from embed_video.admin import AdminVideoMixin


class ProductAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = (
        'title', 'image_data', 'publishDate', 'category', 'format', 'rating', 'price_dollar', 'availability',
        'created_time')

    # fields = ('title', 'image_data', 'publishDate', "category", 'format', 'rating', 'price_dollar', 'availability',)

    def price_dollar(self, obj):
        if obj.discount_price:
            return mark_safe("$" + str(obj.discount_price))
        else:
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


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'product_cover', 'product_title', 'score', 'user', 'created_time'
    )

    def product_title(self, obj):
        title = obj.product.title
        return mark_safe(str(title))

    def product_cover(self, obj):
        res = obj.product.image.url
        # return mark_safe(str(res))
        return mark_safe(u'<img src="%s" width="100px" />' % res)


admin.site.register(Score, ScoreAdmin)
