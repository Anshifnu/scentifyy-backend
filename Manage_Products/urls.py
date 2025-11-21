from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('manage/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('manage/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]
