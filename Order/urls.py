from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView,ClearCartView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('clear/cart/',ClearCartView.as_view(),name='clear_cart'),
]