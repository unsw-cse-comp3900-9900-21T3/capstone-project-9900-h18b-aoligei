from django.contrib import admin
from Product.models import Category, Product, Rating, Format, Availability

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Format)
admin.site.register(Availability)