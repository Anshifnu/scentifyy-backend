from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order
from .serializers import OrderSerializer
from Cart.models import CartItem
from django_filters.rest_framework import DjangoFilterBackend
from Common.permissions import IsUser


class OrderListCreateAPIView(APIView):
    """GET: List all user's orders | POST: Create new order"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-date')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("Incoming order data:", request.data)
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """GET: Retrieve one order | PATCH: Update status (admin)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Allow user to update only status if needed (optional)
        status_value = request.data.get('status')
        if status_value:
            order.status = status_value
            order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ClearCartView(APIView):
    def delete(self, request):
        user = request.user
        CartItem.objects.filter(user=user).delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)

