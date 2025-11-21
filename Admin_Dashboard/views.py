from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from Common.permissions import IsAdmin
from rest_framework.permissions import IsAdminUser


User = get_user_model()

class AdminUsersView(APIView):
    permission_classes = [IsAdmin,IsAdminUser]
    def get(self, request):
        users = User.objects.prefetch_related(
            "orders__items__product"
        ).all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

