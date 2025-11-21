from django.db import models
from Brand.models import Brand

class Product(models.Model):
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()

    def __str__(self):
        return f"Image for {self.product.name}" 
