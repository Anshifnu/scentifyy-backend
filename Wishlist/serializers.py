from rest_framework import serializers
from .models import Wishlist
from Product.models import Product,image

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = image
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    
    brand = serializers.CharField(source='brand.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)  

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'brand', 'images'
        ]





class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'added_at']
