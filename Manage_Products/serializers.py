# Product/serializers.py
from rest_framework import serializers
from Product.models import Product, image
from Brand.models import Brand

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    gallery = serializers.ListField(
        child=serializers.URLField(), write_only=True, required=False
    )
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "brand",
            "name",
            "description",
            "price",
            "stock",
            "is_active",
            "images",
            "gallery",
        ]

    def create(self, validated_data):
        gallery_data = validated_data.pop("gallery", [])
        product = Product.objects.create(**validated_data)
        for url in gallery_data:
            image.objects.create(product=product, image=url)
        return product

    def update(self, instance, validated_data):
        gallery_data = validated_data.pop("gallery", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if gallery_data is not None:
            instance.images.all().delete()
            for url in gallery_data:
                image.objects.create(product=instance, image=url)
        return instance
