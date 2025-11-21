from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CartItem
from .serializers import CartItemSerializer
from Product.models import Product
from Common.permissions import IsUser

class CartAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # 🧠 GET - Get all cart items for logged-in user
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🛒 POST - Add a product to cart
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            qty = serializer.validated_data.get('qty', 1)

            # Check if already in cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, product=product,
                defaults={'qty': qty}
            )

            # If exists, just update quantity
            if not created:
                cart_item.qty += qty
                cart_item.save()

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✏️ PATCH - Update quantity of specific cart item
    def patch(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ❌ DELETE - Remove item from cart
    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)

