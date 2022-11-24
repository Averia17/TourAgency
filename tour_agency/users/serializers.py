import datetime
import hashlib

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.constants import HASH_SALT
from orders.serializers import OrderDetailSerializer
from users.models import User


class UserRegisterSerializer(ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ("id", "email", "password")


class UserDetailSerializer(ModelSerializer):
    orders = OrderDetailSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "is_staff", "is_manager", "orders")


class PasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        hash_str = data["email"] + str(datetime.date.today()) + HASH_SALT
        if data["token"] != hashlib.sha256(hash_str.encode()).hexdigest():
            raise serializers.ValidationError({"token": "token is not valid"})
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({"id": self.user.id})
        return data
