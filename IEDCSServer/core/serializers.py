from rest_framework import serializers
from .models import User, Player, Device, Content, Purchase


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
