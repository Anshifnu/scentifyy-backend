from django.urls import path
from .views import BrandListCreateView,BrandDetailView

urlpatterns = [
    path("brand/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("brand/<int:pk>/", BrandDetailView.as_view(), name="brand-detail"),



]