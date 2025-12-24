

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class RazorpayPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("CREATED", "CREATED"),
            ("PAID", "PAID"),
            ("FAILED", "FAILED"),
        ],
        default="CREATED",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

