from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model
User = get_user_model()




class RegisterView(APIView):
    def post(self,request):
        serilizer=RegisterSerializer(data=request.data)
        if serilizer.is_valid():
            user=serilizer.save()

            subject = "Welcome to  Scentifyy!"
            message = f"Hi {user.username},\n\nThank you for registering with us! 🎉\nWe're excited to have you on board.\n\nEnjoy shopping!\n\n- The Team Scentifyy"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            

            return Response({"message":"User Registered Succesfully"},status=status.HTTP_201_CREATED)
        
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            
            refresh = RefreshToken.for_user(user)

            
            access_token = refresh.access_token
            access_token['username'] = user.username
            access_token['email'] = user.email
            access_token['role']=user.role
            access_token['isBlock']=user.isBlock

            return Response({
                
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)


            
        



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")  # 👈 frontend sends refresh token

        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=400)

        return Response({"detail": "Logout successful"}, status=205)






class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

        # Send email
        send_mail(
            "Reset your password",
            f"Click here to reset your password: {reset_link}",
            "no-reply@yourapp.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Reset link sent to email"}, status=200)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)

        except:
            return Response({"error": "Invalid link"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response({"message": "Password reset successful"}, status=200)




class CustomTokenRefreshView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=400)
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh["user_id"]
            print(user_id)
            user = User.objects.get(id=user_id)
            
            # Create new access token
            access = refresh.access_token
            access["username"] = user.username
            access["email"] = user.email
            access["role"] = user.role
            access['isBlock']=user.isBlock
            return Response({
                "access": str(access),
                "refresh": str(refresh_token)
            }, status=200)

        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=401)
        


