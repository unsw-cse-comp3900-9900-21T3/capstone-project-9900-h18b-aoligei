from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'image_data', 'publishDate', 'category', 'format', 'rating', 'price_dollar', 'availability',
        'created_time')
    # fields = ('title', 'image', 'publishDate', "category", 'format', 'rating', 'price', 'availability',)

    # def price(self, obj):
    #     return mark_safe(obj.price)
    def price_dollar(self, obj):
        return mark_safe("$" + str(obj.price))

    def image_data(self, obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.image.url)

    #
    # def publish_date(self, obj):
    #     return mark_safe(obj.publishDate)
    #
    # def category(self, obj):
    #     return mark_safe(obj.category)
    #
    # def format(self, obj):
    #     return mark_safe(obj.format)
    #
    # def rating(self, obj):
    #     return mark_safe(obj.rating)
    #
    image_data.short_description = u'image desc'
    # price_dollar.short_description = u'price'
    # publish_date.short_description = u'Publish Date'
    # category.short_description = u'category'
    # format.short_description = u'format'
    # rating.short_description = u'rating'


admin.site.site_header = "Aoligei E-Commerce Administration"
admin.site.site_title = "Aoligei E-Commerce Administration"
admin.site.index_title = "Aoligei E-Commerce Administration"

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating)
admin.site.register(Format)
admin.site.register(Availability)
