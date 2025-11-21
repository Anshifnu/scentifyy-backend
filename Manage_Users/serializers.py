from rest_framework import serializers
from User.models import User

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active", "isBlock"]
