
from django.urls import path

from .views import ManageOrdersView,UpdateOrderStatusView

urlpatterns = [
    path('manage/orders/', ManageOrdersView.as_view(), name='admin_manage_orders'),
     path('manage/orders/<int:order_id>/', UpdateOrderStatusView.as_view(), name='admin_manage_orders'),
]

