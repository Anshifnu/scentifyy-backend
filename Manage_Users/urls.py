from django.urls import path
from .views import ManageUsersView, ManageUserDetailView

urlpatterns = [
    path("manage/users/", ManageUsersView.as_view(), name="manage_users"),
    path("manage/users/<int:pk>/", ManageUserDetailView.as_view(), name="manage_user_detail"),
]
