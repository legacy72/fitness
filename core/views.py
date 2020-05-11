from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset


class ProbeUserViewSet(viewsets.ModelViewSet):
    serializer_class = ProbeUserSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'probe_type', 'value', 'created_at']

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Probe.objects.filter(user_id=user_id).all()
        return queryset


class ProbeViewSet(viewsets.ModelViewSet):
    serializer_class = ProbeSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Probe.objects.all()
        return queryset


class ProbeTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProbeTypeSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = ProbeType.objects.all()
        return queryset
