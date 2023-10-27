from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.viewsets import GenericViewSet

from api.permissions import ReadOnly, IsOwnSelf
from api.serializers import UserSerializer, NewUserSerializer, GroupSerializer, PasswordSerializer

from django.contrib.auth import authenticate

import requests


# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    username = data['username']
    password = data['password']
    group = data['group']

    # Valid existing group
    if group not in Group.objects.filter().values_list('name', flat=True):
        return Response(data={'error': 'Invalid group'}, status=status.HTTP_400_BAD_REQUEST)

    group = Group.objects.get(name=group)
    new_user = User.objects.create_user(username=username, email=username, password=password)

    new_user.groups.add(group)
    data = NewUserSerializer(new_user)
    return Response(data=data.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)

    return Response(data={'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, ])
def proxy_ghibli(request):
    base_url = 'https://ghibliapi.vercel.app/'
    if request.user.groups:
        group = request.user.groups.first()
        ghibli_name = group.name.lower()
        url = base_url + ghibli_name
        response = requests.get(url)
        return Response(data=response.json(), status=status.HTTP_200_OK)

    return Response(data={'error': 'User has no group'}, status=status.HTTP_409_CONFLICT)


class UserViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdminUser|ReadOnly]

    @action(detail=True, methods=['POST'], serializer_class=PasswordSerializer,  permission_classes=[IsOwnSelf])
    def change_password(self, request, pk=None):
        user = self.get_object()
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], serializer_class=GroupSerializer, permission_classes=[IsAdminUser|IsOwnSelf])
    def change_group(self, request, pk=None):
        user = self.get_object()
        if request.data['group'] not in Group.objects.filter().values_list('name', flat=True):
            return Response(data={'error': 'Invalid group'}, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.get(name=request.data['group'])
        user.groups.clear()
        user.groups.add(group)
        return Response(status=status.HTTP_204_NO_CONTENT)