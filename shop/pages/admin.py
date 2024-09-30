from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html

from .models import Category, Tag, Brand, Product, Color, ProductColor, Size, ProductSize, ProductFavorite, ProductImage


# Register your models here.
class DiscountFilter(admin.SimpleListFilter):
    title = 'Discount'
    parameter_name = 'discount'

    def lookups(self, request, model_admin):
        return [
            ('>0', 'Yes')
        ]

    def queryset(self, request, queryset):
        if self.value() == '>0':
            return queryset.filter(discount__gt=0)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'product_count']
    list_display_links = ['pk', 'title']

    def product_count(self, obj):
        return obj.product_set.all().count()


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'product_count']
    list_display_links = ['pk', 'title']

    def product_count(self, obj):
        return obj.product_set.all().count()


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'product_count']
    list_display_links = ['pk', 'title']

    def product_count(self, obj):
        return obj.product_set.all().count()


@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'get_color']
    list_editable = ['title']

    def get_color(self, obj):
        return format_html(f'<div style="width:30px; height:30px; background-color:{obj.color};"></div>')


@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ['pk', 'title']


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    fk_name = 'product'
    extra = 1


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    fk_name = 'product'
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = 'product'
    extra = 3


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'brand', 'category', 'available', 'price', 'discount',
                    'final_price', 'first_photo']
    list_editable = ['price', 'discount', 'available']
    list_display_links = ['pk', 'title']
    list_filter = ['category', DiscountFilter]
    prepopulated_fields = {'slug': ['title']}
    inlines = [ProductColorInline, ProductSizeInline, ProductImageInline]

    def final_price(self, obj):
        disc_price = float(obj.price) - float(obj.price) * obj.discount / 100
        return disc_price

    def first_photo(self, obj):
        try:
            image = obj.images.first().image.url
            return format_html(f'<img src="{image}" width="100">')
        except:
            return '-'



