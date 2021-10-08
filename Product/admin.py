from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability
from django.utils.safestring import mark_safe


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'image_data')
#     readonly_fields = ('image_data',)
#
#     def image_data(self, obj):
#         return mark_safe(u'<img src="%s" width="250px" />' % obj.image.url)
#
#     image_data.short_description = u'image desc'


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Format)
admin.site.register(Availability)
