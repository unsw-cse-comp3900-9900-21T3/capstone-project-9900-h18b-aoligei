from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability, Score, Order, OrderItem, ShippingAddress
from django.utils.safestring import mark_safe
from embed_video.admin import AdminVideoMixin

admin.site.site_header = "Aoligei E-Commerce Administration"
admin.site.site_title = "Aoligei E-Commerce Administration"
admin.site.index_title = "Aoligei E-Commerce Administration"


class ProductAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = (
        'title', 'image_data', 'publishDate', 'category', 'format', 'rating', 'price_dollar', 'availability',
        'created_time')
    list_per_page = 8
    search_fields = ['title', ]

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


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Categories', 'Count')
    search_fields = ['title']
    list_per_page = 20

    def Categories(self, obj):
        return mark_safe(str(obj.title))

    def Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Category, CategoryAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('Rating', 'Count')
    search_fields = ['title']
    list_per_page = 20

    def Rating(self, obj):
        return mark_safe(str(obj.title))

    def Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Rating, RatingAdmin)


class FormatAdmin(admin.ModelAdmin):
    list_display = ('Format', 'Count')
    search_fields = ['title']
    list_per_page = 20

    def Format(self, obj):
        return mark_safe(str(obj.title))

    def Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Format, FormatAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('Availability', 'Count')
    search_fields = ['title']
    list_per_page = 20

    def Availability(self, obj):
        return mark_safe(str(obj.title))

    def Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Availability, AvailabilityAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'product_cover', 'product_title', 'score_mark', 'user', 'created_time'
    )
    list_per_page = 8

    def product_title(self, obj):
        title = obj.product.title
        return mark_safe(str(title))

    def product_cover(self, obj):
        res = obj.product.image.url
        # return mark_safe(str(res))
        return mark_safe(u'<img src="%s" width="100px" />' % res)

    def score_mark(self, obj):
        temp_score = int(obj.score)
        if temp_score <= 0.5:
            temp_score = "" + str(obj.score)
        elif temp_score <= 1.0:
            temp_score = "⭐ " + str(obj.score)
        elif temp_score <= 1.5:
            temp_score = "⭐ " + str(obj.score)
        elif temp_score <= 2.0:
            temp_score = "⭐⭐ " + str(obj.score)
        elif temp_score <= 2.5:
            temp_score = "⭐⭐ " + str(obj.score)
        elif temp_score <= 3.0:
            temp_score = "⭐⭐⭐ " + str(obj.score)
        elif temp_score <= 3.5:
            temp_score = "⭐⭐⭐ " + str(obj.score)
        elif temp_score <= 4.0:
            temp_score = "⭐⭐⭐⭐ " + str(obj.score)
        elif temp_score <= 4.5:
            temp_score = "⭐⭐⭐⭐ " + str(obj.score)
        else:
            temp_score = "⭐⭐⭐⭐⭐ " + str(obj.score)
        return mark_safe(temp_score)


admin.site.register(Score, ScoreAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'total_quantity', 'total_price', 'customer', 'complete', 'date_ordered',
    )
    exclude = ['transaction_id', 'customer', 'complete',]

    readonly_fields = ['transaction_id', 'total_quantity', 'total_price', 'customer', 'complete', 'date_ordered',]
    list_per_page = 8

    def total_quantity(self, obj):
        return mark_safe(str(obj.get_cart_items))

    def total_price(self, obj):
        return mark_safe(str(obj.get_cart_total))


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'product_title', 'product_cover', 'price', 'quantity', 'total', 'customer', 'complete',
        'date_added',
    )
    list_per_page = 8

    readonly_fields = ['transaction_id', 'product_title', 'product_cover', 'price', 'quantity', 'total', 'customer',
                       'complete',
                       'date_added', ]

    def product_title(self, obj):
        return mark_safe(str(obj.product.title))

    def product_cover(self, obj):

        return mark_safe(u'<img src="%s" width="100px" />' % (obj.product.image.url))

    def price(self, obj):
        if obj.product.discount_price:
            return mark_safe("$" + str(obj.product.discount_price))
        else:
            return mark_safe("$" + str(obj.product.price))

    def transaction_id(self, obj):
        return mark_safe(str(obj.order.transaction_id))

    def customer(self, obj):
        return mark_safe(str(obj.order.customer))

    def total(self, obj):
        total = obj.get_total
        return mark_safe(str(total))

    def complete(self, obj):
        return mark_safe(obj.order.complete)


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
