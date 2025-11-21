# order/models.py
from django.db import models
from django.contrib.auth import get_user_model
from Product.models import Product

User = get_user_model()

class ShippingInfo(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}, {self.city}"


class PaymentInfo(models.Model):
    card_number = models.CharField(max_length=20)
    expiry = models.CharField(max_length=10)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"**** **** **** {self.card_number[-4:]}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipping", "Shipping"),
        ("processing", "Processing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    shipping_info = models.OneToOneField(ShippingInfo, on_delete=models.CASCADE)
    payment_info = models.OneToOneField(PaymentInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.qty}"

