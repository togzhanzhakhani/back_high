from rest_framework import viewsets, permissions
from django.shortcuts import render
from .models import Product, Shop, Category
from .serializers import ProductSerializer, ShopSerializer, CategorySerializer
from django.core.cache import cache

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        cache_key = 'shop_list'
        shops = cache.get(cache_key)
        if not shops:
            shops = list(super().get_queryset())
            cache.set(cache_key, shops, timeout=60 * 15) 
        return shops

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            categories = list(super().get_queryset())
            cache.set(cache_key, categories, timeout=60 * 15)
        return categories


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('shop', 'category').all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id')
        category_id = self.request.query_params.get('category_id')
        cache_key = f'product_list_{shop_id}_{category_id}'
        products = cache.get(cache_key)

        if products is None: 
            queryset = self.queryset 

            if shop_id and category_id:
                queryset = queryset.filter(shop_id=shop_id, category_id=category_id)
            elif shop_id:
                queryset = queryset.filter(shop_id=shop_id)
            elif category_id:
                queryset = queryset.filter(category_id=category_id)

            products = list(queryset)
            cache.set(cache_key, products, timeout=60 * 15) 
        
        return products  
