from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Brand
from .serializers import BrandSerializer
from Common.permissions import IsUser,IsAdmin


# List all brands and create a new brand
class BrandListCreateView(APIView):

    

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific brand
class BrandDetailView(APIView):


    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return None

    def get(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            return Response({"detail": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            return Response({"detail": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            return Response({"detail": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

