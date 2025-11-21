from rest_framework import serializers
from Order.models import Order, OrderItem
from Product.models import Product
from User.models import User   

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "name", "qty", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "date", "status", "items"]


class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "orders"]
