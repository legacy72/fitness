from rest_framework import filters
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.all()
        return User.objects.filter(
                pk=user.pk,
            ).all()


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset


class ProbeUserViewSet(viewsets.ModelViewSet):
    """
    params: start_date - отфильтровать по пробам, которые были сделаны после данной даты
    """
    serializer_class = ProbeUserSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'name', 'input_method']

    def get_queryset(self):
        queryset = ProbeType.objects.all()
        return queryset


class ChatViewSet(viewsets.ModelViewSet):
    """
    params: user_id - отфильтровать чаты по тем, в которых участвовал данный юзер
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Chat.objects.all()
        return Chat.objects.filter(members__in=[user])


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'chat', 'author', 'is_read']

    def get_queryset(self):
        return Message.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'role', 'first_name', 'last_name', 'date_of_birth', 'gender', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Profile.objects.all()
        return Profile.objects.filter(
                user=user,
            ).all()
