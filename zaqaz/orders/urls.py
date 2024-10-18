from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import OrderCreateView, OrderStatusUpdateView, OrderCancelView, OrderDetailView, AdminOrderListView

router = SimpleRouter()

urlpatterns = [
    path('admin/orders/', AdminOrderListView.as_view(), name='admin_order_list'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail_delete'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='update_order_status'),
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view(), name='cancel_order'),
]

urlpatterns += router.urls
