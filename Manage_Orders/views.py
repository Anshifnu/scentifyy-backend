
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserWithOrdersSerializer
from rest_framework import status
from Order.models import Order
from .serializers import OrderStatusUpdateSerializer
from Common.permissions import IsAdmin
from rest_framework.permissions import IsAdminUser


User = get_user_model()

class ManageOrdersView(APIView):

    permission_classes=[IsAdmin,IsAdminUser]
    def get(self, request):
        users = User.objects.prefetch_related('orders__items__product').all()
        serializer = UserWithOrdersSerializer(users, many=True)
        return Response(serializer.data)


class UpdateOrderStatusView(APIView):
    permission_classes=[IsAdmin,IsAdminUser]
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Status updated successfully", "order": serializer.data})

        print(serializer.errors)  # <-- ADD THIS
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
