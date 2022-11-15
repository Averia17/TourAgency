from urllib.parse import urlencode

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import mixins, serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer
from users.services import google_validate_id_token


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        id_token = request.headers.get("Authorization")
        google_validate_id_token(id_token)
        email = request.data["email"]
        # create user if not exist
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "password": make_password(BaseUserManager().make_random_password())
            },
        )
        # generate token without username & password
        token = RefreshToken.for_user(user)
        response = {
            "id": user.pk,
            "access": str(token.access_token),
            "refresh": str(token),
        }
        return Response(response)
