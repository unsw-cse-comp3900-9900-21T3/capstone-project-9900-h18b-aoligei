from django.db import models
from django.utils.safestring import mark_safe


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


class Format(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'format'
        verbose_name_plural = 'formats'

    def __str__(self):
        return self.title


class Rating(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return self.title


class Availability(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'availability'
        verbose_name_plural = 'availabilities'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(u'image', upload_to='products/%Y/%m/%d', blank=True)

    # def image_data(self, obj):
    #     return mark_safe(u'<img src="%s" width="100px" />' % obj.image.url)


    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, null=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True)

    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    publishDate = models.DateField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
