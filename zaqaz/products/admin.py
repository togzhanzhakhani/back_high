from django.contrib import admin
from .models import Shop, Category, Product

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop', 'category', 'price', 'discount')
    search_fields = ('name', 'description')
    list_filter = ('shop', 'category')
