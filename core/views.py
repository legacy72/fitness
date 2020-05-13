from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(
            {'username': user.username}, status=status.HTTP_201_CREATED, headers=headers
        )


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset


class ProbeUserViewSet(viewsets.ModelViewSet):
    """
    params: start_date - отфильтровать по пробам, которые были сделаны после данной даты
    """
    serializer_class = ProbeUserSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'probe_type', 'value', 'created_at']

    def get_queryset(self):
        user_id = self.request.user.id
        start_date = self.request.GET.get('start_date', "1970-01-01")
        queryset = Probe.objects.filter(
            user_id=user_id,
            created_at__gte=start_date,
        ).all()
        return queryset


class ProbeViewSet(viewsets.ModelViewSet):
    """
    params: start_date - отфильтровать по пробам, которые были сделаны после данной даты
    """
    serializer_class = ProbeSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'probe_type', 'value', 'created_at']

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', "1970-01-01")
        queryset = Probe.objects.filter(
            created_at__gte=start_date,
        ).all()
        return queryset


class ProbeTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProbeTypeSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'name', 'input_method']

    def get_queryset(self):
        queryset = ProbeType.objects.all()
        return queryset
