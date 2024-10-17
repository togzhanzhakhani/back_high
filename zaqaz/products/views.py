from rest_framework import viewsets, permissions
from .models import Product, Shop, Category
from .serializers import ProductSerializer, ShopSerializer, CategorySerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
