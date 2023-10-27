from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, register, login, proxy_ghibli

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ghibli/', proxy_ghibli, name='ghibli'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
