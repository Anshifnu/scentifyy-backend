from rest_framework import serializers
from .models import CartItem
from Product.models import Product, image  # import Product and image models

class ProductImageSerializer(serializers.ModelSerializer):
    """Serialize individual product images"""
    class Meta:
        model = image
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    """Serialize full product info with all images"""
    brand = serializers.CharField(source='brand.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)  # all images

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'brand', 'images'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # nested product data
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'qty', 'added_at']
