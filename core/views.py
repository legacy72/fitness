from django.shortcuts import render
from rest_framework import status, viewsets

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
