from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_order_items', 'total_price', 'shipping_address', 'created_at', 'status')
    search_fields = ('status',)
    inlines = [OrderItemInline]

    def get_order_items(self, obj):
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in obj.order_items.all()])

    get_order_items.short_description = 'Order Items'

