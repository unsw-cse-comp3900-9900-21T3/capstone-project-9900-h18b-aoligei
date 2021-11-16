from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability, Score, Order, OrderItem, ShippingAddress
from django.utils.safestring import mark_safe
from embed_video.admin import AdminVideoMixin

admin.site.site_header = "Aoligei E-Commerce Administration"
admin.site.site_title = "Aoligei E-Commerce Administration"
admin.site.index_title = "Aoligei E-Commerce Administration"


class ProductAdmin(AdminVideoMixin, admin.ModelAdmin):
    ''' manage the features of product in the admin system '''
    # list display product feature in product list page
    list_display = (
        'title', 'image_data', 'publishDate', 'category', 'format', 'rating', 'price_dollar', 'availability',
        'score_avg', 'score_count',
        'updated_time')
    list_per_page = 10
    # setting the search filtering fields in the admin system
    search_fields = ['title', 'category__title', 'format__title', 'rating__title', 'availability__title',
                     'price', 'discount_price']

    def price_dollar(self, obj):
        if obj.discount_price:
            return mark_safe("$" + str(obj.discount_price))
        else:
            return mark_safe("$" + str(obj.price))

    def image_data(self, obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.image.url)

    def score_avg(self, obj):
        if obj.get_avg_score:
            return mark_safe(round(float(obj.get_avg_score), 2))

    def score_count(self, obj):
        return mark_safe(obj.score_count)

    image_data.short_description = u'image desc'
    price_dollar.short_description = u'price'


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    ''' manage the features of category in the admin system '''
    list_display = ('Categories', 'Product_Count')
    search_fields = ['title']
    list_per_page = 20

    def Categories(self, obj):
        return mark_safe(str(obj.title))

    def Product_Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Category, CategoryAdmin)


class RatingAdmin(admin.ModelAdmin):
    ''' manage the features of rating in the admin system '''
    list_display = ('Rating', 'Product_Count')
    search_fields = ['title']
    list_per_page = 20

    def Rating(self, obj):
        return mark_safe(str(obj.title))

    def Product_Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Rating, RatingAdmin)


class FormatAdmin(admin.ModelAdmin):
    ''' manage the features of format in the admin system '''
    list_display = ('Format', 'Product_Count')
    search_fields = ['title']
    list_per_page = 20

    def Format(self, obj):
        return mark_safe(str(obj.title))

    def Product_Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Format, FormatAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    ''' manage the features of Availability in the admin system '''
    list_display = ('Availability', 'Product_Count')
    search_fields = ['title']
    list_per_page = 20

    def Availability(self, obj):
        return mark_safe(str(obj.title))

    def Product_Count(self, obj):
        return mark_safe(str(obj.total_items))


admin.site.register(Availability, AvailabilityAdmin)


class ScoreAdmin(admin.ModelAdmin):
    ''' manage the features of Score in the admin system '''
    list_display = (
        'product_cover', 'product_title', 'score_mark', 'user', 'created_time'
    )
    search_fields = ['score', 'user__username', 'product__title']
    list_per_page = 10

    def product_title(self, obj):
        title = obj.product.title
        return mark_safe(str(title))

    def product_cover(self, obj):
        res = obj.product.image.url
        # return mark_safe(str(res))
        return mark_safe(u'<img src="%s" width="100px" />' % res)

    def score_mark(self, obj):
        temp_score = float(obj.score)
        return mark_safe(temp_score)


admin.site.register(Score, ScoreAdmin)


class OrderAdmin(admin.ModelAdmin):
    ''' manage the features of Order in the admin system '''
    list_display = (
        'transaction_Id', 'total_quantity', 'total_price', 'customer', 'complete', 'date_ordered',
    )
    # setting item numbers in a single page
    list_per_page = 15

    exclude = ['transaction_id', 'customer', 'complete', ]

    readonly_fields = ['transaction_Id', 'total_quantity', 'total_price', 'customer', 'complete', 'date_ordered', ]

    def transaction_Id(self, obj):
        if obj.transaction_id != None and obj.transaction_id != 'NULL':
            return mark_safe(obj.transaction_id)
        # else:
        #     obj.delete()

    def total_quantity(self, obj):
        if obj:
            return mark_safe(str(obj.get_cart_items))

    def total_price(self, obj):
        if obj:
            return mark_safe("$" + str(obj.get_cart_total))

    search_fields = ['transaction_id', 'complete', 'customer__username', ]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    ''' manage the features of OrderItem in the admin system '''
    list_display = (
        'transaction_id', 'product_title', 'product_cover', 'price', 'quantity', 'total', 'customer', 'completed',
        'date_added',
    )
    list_per_page = 8

    search_fields = ['order__transaction_id', 'product__title', 'product__price', 'product__discount_price', 'quantity',
                     'order__complete', 'order__customer__username']

    exclude = ['product', 'order', 'quantity', ]

    readonly_fields = ['transaction_id', 'product_title', 'product_cover', 'price', 'quantity', 'total', 'customer',
                       'completed',
                       'date_added', ]

    def product_title(self, obj):
        if obj.product:
            return mark_safe(str(obj.product.title))

    def product_cover(self, obj):
        if obj.product:
            return mark_safe(u'<img src="%s" width="100px" />' % (obj.product.image.url))

    def price(self, obj):
        if obj.product.discount_price:
            return mark_safe("$" + str(obj.product.discount_price))
        elif obj.product.price:
            return mark_safe("$" + str(obj.product.price))

    def transaction_id(self, obj):
        if obj.order:
            return mark_safe(obj.order.transaction_id)

    def customer(self, obj):
        if obj.order:
            return mark_safe(str(obj.order.customer))
        else:
            obj.delete()

    def total(self, obj):
        if obj:
            total = obj.get_total
            return mark_safe("$" + str(total))

    def completed(self, obj):
        if obj.order:
            return mark_safe(obj.order.complete)


admin.site.register(OrderItem, OrderItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    ''' manage the features of shipping address in the admin system '''
    list_display = ['customer', 'transaction_Id', 'address', 'city', 'state', 'country', 'zipcode', 'date_added']
    search_fields = ['customer__username', 'order__transaction_id', 'address', 'city', 'state', 'country', 'zipcode',
                     'date_added']
    list_per_page = 15

    exclude = ['customer', 'city', 'address', 'state', 'zipcode', 'order', 'country']
    #
    readonly_fields = ['customer', 'transaction_Id', 'address', 'city', 'state', 'country', 'zipcode', 'date_added']

    def transaction_Id(self, obj):
        if obj.order:
            return mark_safe(obj.order.transaction_id)
        else:
            obj.delete()


admin.site.register(ShippingAddress, ShippingAddressAdmin)
