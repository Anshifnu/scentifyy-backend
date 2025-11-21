from django.urls import path
from .views import AdminUsersView

urlpatterns = [
    path("dashboard/", AdminUsersView.as_view(),name="dashboard_view")

   
    
]