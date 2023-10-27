from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer


class NewUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)


class GroupSerializer(serializers.Serializer):
    group = serializers.CharField(max_length=50)


class UserSerializer(ModelSerializer):
    groups = StringRelatedField(many=True)

    class Meta:
        model = User
        read_only_fields = ['username', ]
        fields = ['id', 'username', 'email', 'groups', ]

