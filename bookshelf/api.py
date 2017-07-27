from django.conf.urls import url, include
from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets
from .views import api_saveSelf
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'is_staff', 'is_active', 'last_login', 'first_name', 'last_name', 'is_superuser',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
