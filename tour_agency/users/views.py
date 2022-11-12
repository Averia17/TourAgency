from urllib.parse import urlencode

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from tour_agency.settings import BASE_FRONTEND_URL, BASE_BACKEND_URL
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer
from users.services import google_get_access_token, google_get_user_info


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class GoogleLoginView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.data.get("code")
        error = request.data.get("error")
        login_url = f"{BASE_FRONTEND_URL}/login"
        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")
        domain = BASE_BACKEND_URL
        api_uri = reverse("login-with-google")
        redirect_uri = f"{domain}{api_uri}"
        access_token = google_get_access_token(code, redirect_uri)
        data = google_get_user_info(access_token)
        # create user if not exist
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            user = User.objects.create_user(
                data["email"], make_password(BaseUserManager().make_random_password())
            )
        # generate token without username & password
        token = RefreshToken.for_user(user)
        response = {
            "id": user.pk,
            "access_token": str(token.access_token),
            "refresh_token": str(token),
        }
        return Response(response)
