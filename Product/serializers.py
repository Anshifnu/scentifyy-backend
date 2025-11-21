from rest_framework import serializers
from .models import Product, image
from Brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)  # remove read_only=True
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'images','is_active','brand']

    def update(self, instance, validated_data):
        # Handle nested images
        images_data = validated_data.pop('images', None)

        # Update main product fields
        instance = super().update(instance, validated_data)

        if images_data is not None:
            # Remove old images
            instance.images.all().delete()
            # Add new images
            for img_data in images_data:
                image.objects.create(product=instance, **img_data)

        return instance
