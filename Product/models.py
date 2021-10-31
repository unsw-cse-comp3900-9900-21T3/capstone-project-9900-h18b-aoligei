from django.db import models
from django.utils.safestring import mark_safe
from mdeditor.fields import MDTextField, MDTextFormField
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.aggregates import Count


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    @property
    def total_items(self):
        total = self.product_set.all()
        return len(total)


class Format(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'format'
        verbose_name_plural = 'formats'

    def __str__(self):
        return self.title

    @property
    def total_items(self):
        total = self.product_set.all()
        return len(total)


class Rating(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return self.title

    @property
    def total_items(self):
        total = self.product_set.all()
        return len(total)


class Availability(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'availability'
        verbose_name_plural = 'availabilities'

    def __str__(self):
        return self.title

    @property
    def total_items(self):
        total = self.product_set.all()
        return len(total)


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()

    image = models.ImageField(u'image', upload_to='products/%Y/%m/%d', default='media/logo.png')
    # def image_data(self, obj):
    #     return mark_safe(u'<img src="%s" width="100px" />' % obj.image.url)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, null=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True)
    publishDate = models.DateField()

    # description = models.TextField(blank=True)
    description = MDTextField(blank=True, null=True)
    trailer = EmbedVideoField(blank=True, null=True)
    details = MDTextField(blank=True, null=True)

    available = models.BooleanField(default=True)
    digital = models.BooleanField(default=False, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)

    # updated_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Product:getProduct', args=[self.id])


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ('-date_ordered',)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return float(total)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    @property
    def get_total(self):
        if self.product.discount_price:
            total = self.product.discount_price * self.quantity
            return total
        total = self.product.price * self.quantity
        return float(total)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Score(models.Model):
    score = models.FloatField(null=True, default=1.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time',)
        verbose_name = 'score'

    def __float__(self):
        return self.score
