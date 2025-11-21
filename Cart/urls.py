from django.urls import path
from .views import CartAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view()),        # GET, POST
    path('cart/<int:pk>/', CartAPIView.as_view()) # PATCH, DELETE
    
]