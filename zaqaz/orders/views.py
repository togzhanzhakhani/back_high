from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order
from .serializers import OrderSerializer

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)  
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk):
        self.check_permissions(request)  
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({"message": f"Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def check_permissions(self, request):
        if not request.user.is_staff:
            self.permission_denied(request)


class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]  

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status  = request.data.get('status')

        if order.status in ['delivered', 'cancelled', 'refunded']:
            return Response({"error": "Cannot change status of completed or cancelled orders"}, 
            status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status 
        if new_status  == 'delivered':
            order.is_paid = True 
        order.save()

        return Response(OrderSerializer(order).data)
    

class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != 'pending':
            return Response({"error": "Only pending orders can be cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()

        return Response({"status": "cancelled"})