from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'user'},
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password':{'required':True},
            'confirm_password':{'required': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data




class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No user with this email")

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        if len(password) < 6:
            raise serializers.ValidationError("Password too short")
        return attrs

