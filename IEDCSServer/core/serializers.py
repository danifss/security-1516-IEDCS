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



# class AttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attribute
#
# class ProfileSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#     attributes = AttributeSerializer(many=True)
#
#     class Meta:
#         model = Profile
#
# class RelationSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#     attributes = AttributeSerializer(many=True)
#
#     class Meta:
#         model = Profile
#         exclude = ("connections",)

