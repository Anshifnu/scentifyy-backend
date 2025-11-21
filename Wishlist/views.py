from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Wishlist
from .serializers import WishlistSerializer
from Common.permissions import IsUser
class WishlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsUser]

    # 🧠 GET: Get all wishlist items for logged-in user
    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🩷 POST: Add a product to wishlist
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']

            # Prevent duplicate wishlist entries (unique_together already ensures)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user, product=product
            )

            if not created:
                return Response({"message": "Product already in wishlist"}, status=status.HTTP_200_OK)

            return Response(WishlistSerializer(wishlist_item).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        try:
            wishlist_item = Wishlist.objects.get(pk=pk, user=request.user)
        except Wishlist.DoesNotExist:
            return Response({"error": "Item not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()
        return Response({"message": "Item removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)

