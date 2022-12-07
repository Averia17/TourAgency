import datetime
import hashlib

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.constants import HASH_SALT
from tour_agency.settings import BASE_FRONTEND_URL
from users.models import User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterSerializer,
    PasswordSerializer,
    UserDetailSerializer,
)
from users.services import google_validate_id_token
from tour_agency.tasks import send_user_email


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=["GET"], serializer_class=UserDetailSerializer, permission_classes=[IsAuthenticated])
    def my(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def has_admin_access(self, request):
        return Response(request.user.is_staff or request.user.is_manager)


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


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, email=data["email"])
        user.set_password(data["new_password"])
        user.save()
        return Response(status=status.HTTP_200_OK)


class SendResetEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        hash_str = email + str(datetime.date.today()) + HASH_SALT
        email_hash = hashlib.sha256(hash_str.encode()).hexdigest()
        send_user_email.delay(
            user.email,
            "Reset password",
            render_to_string(
                "reset_password.html",
                {
                    "link": f"{BASE_FRONTEND_URL}/reset/?token={email_hash}&email={email}"
                },
            ),
        )
        return Response(status=status.HTTP_200_OK)
