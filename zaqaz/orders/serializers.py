from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'created_at', 'status', 'shipping_address', 'is_paid']
        read_only_fields = ['user', 'total_price', 'is_paid']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.total_price = sum(item.product.discounted_price * item.quantity for item in order.order_items.all())
        order.save()
        return order
