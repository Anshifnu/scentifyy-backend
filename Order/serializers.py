from rest_framework import serializers
from .models import ShippingInfo, PaymentInfo, Order, OrderItem
from Product.models import Product

class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = ['full_name', 'address', 'city', 'postal_code', 'country']


class PaymentInfoSerializer(serializers.ModelSerializer):
    # never return full card details in response
    class Meta:
        model = PaymentInfo
        fields = ['card_number', 'expiry', 'cvv']


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    product_name = serializers.CharField(source='product.name', read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        first_image = obj.product.images.first()
        if first_image:
            return first_image.image
        return None

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'qty', 'price', 'image']




class OrderSerializer(serializers.ModelSerializer):
    shipping_info = ShippingInfoSerializer()
    payment_info = PaymentInfoSerializer(required=False,allow_null=True)

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_info', 'payment_info','razorpay_payment_id','payment_method', 'items', 'status', 'date']
        read_only_fields = ['user', 'status', 'date']

    def create(self, validated_data):
        # Extract nested data
        shipping_data = validated_data.pop('shipping_info')
        items_data = validated_data.pop('items')
        payment_data = validated_data.pop('payment_info', None)  # remove safely

    # Create nested objects
        shipping = ShippingInfo.objects.create(**shipping_data)

        if payment_data:  # only create if exists
            payment = PaymentInfo.objects.create(**payment_data)
        else:
            payment = None

    # Create main order
        user = self.context['request'].user
        order = Order.objects.create(
            user=user,
            shipping_info=shipping,
            payment_info=payment,
            **validated_data
        )

    # Create order items
        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order
