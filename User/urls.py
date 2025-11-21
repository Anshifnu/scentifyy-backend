from django.urls import path
from .views import RegisterView,LoginView,LogoutView
from .views import CustomTokenRefreshView,ForgotPasswordView,ResetPasswordView

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/token/refresh/',CustomTokenRefreshView.as_view(),name='refresh_token'),
    path("user/password-reset/", ForgotPasswordView.as_view()),
    path("user/reset-password/<uid>/<token>/", ResetPasswordView.as_view()),
]