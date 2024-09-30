from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    short_description = models.TextField(default='Short description')
    description = models.TextField(default='Main description')
    information = models.TextField(default='Additional info')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(verbose_name='Процент скидки')
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sku = models.CharField(max_length=250, blank=True, null=True)
    sales = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=10)

    def get_discount_price(self):
        disc_price = float(self.price) - float(self.price) * self.discount / 100
        return disc_price

    def get_first_photo(self):
        if len(self.images.all()) > 0:
            return self.images.first().image.url
        else:
            return 'https://pubshamrock.com/wp-content/uploads/2023/04/skoro-zdes-budet-foto.jpg'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=250)
    color = ColorField(default='#ff000')

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class ProductFavorite(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
