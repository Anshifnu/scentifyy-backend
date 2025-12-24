from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from User.models import User
from .serializers import AdminUserSerializer
from Common.permissions import IsAdmin
from django.db.models import Q

class ManageUsersView(APIView):
    permission_classes = [IsAdminUser,IsAdmin]   # only admins allowed

    def get(self, request):
        search=request.query_params.get("search")
        users = User.objects.all().order_by("id")
        if search:
            users = users.filter(
                
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageUserDetailView(APIView):
    permission_classes = [IsAdminUser,IsAdmin]

    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        data = request.data

        # Update Block Status
        if "isBlock" in data:
            user.isBlock = data["isBlock"]

        # Update Role
        if "role" in data:
            user.role = data["role"]

        user.save()
        return Response(AdminUserSerializer(user).data)

