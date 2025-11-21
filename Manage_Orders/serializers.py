# order/serializers.py
from rest_framework import serializers
from Order.models import Order, OrderItem
from Product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # nested product info

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'qty', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField()  # returns username

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'date']

class UserWithOrdersSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'orders']



# order/serializers.py
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
