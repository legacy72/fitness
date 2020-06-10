import random
from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend

from .models import *
from .serializers import *
from .utils.mail import generate_auth_code, send_code


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.all()
        return User.objects.filter(
                pk=user.pk,
            ).all()

    def perform_create(self, serializer):
        # создание пользователя (неактивным)
        user = serializer.save(is_active=False)
        # генерация кода
        code = generate_auth_code()
        # отправка кода подтверждения
        send_code(mail=serializer.data['email'], code=code)
        # добавлени кода в базу
        auth_code = AuthCode(user=user, code=code)
        auth_code.save()


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
    filter_fields = ['id', 'chat', 'author', 'is_read', 'membership']

    def get_queryset(self):
        return Message.objects.all()

    def perform_create(self, serializer):
        data = serializer.validated_data
        members = data['chat'].members.all()
        if self.request.user not in members:
            raise Exception('Вы не состоите в данном чате')
        serializer.save()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_fields = ['id', 'user', 'role', 'first_name', 'last_name', 'date_of_birth', 'gender', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Profile.objects.all()
        return Profile.objects.filter(
                user=user,
            ).all()


class ActivateUserView(viewsets.ViewSet):
    """
    Вьюшка для активации пользователя

    :param request: code - код активации из сообщения на почте
    :param request: username - логин пользователя
    :return:
    """
    def create(self, request):
        data = request.data
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с данным логином не найден'}, status=status.HTTP_400_BAD_REQUEST)
        auth_code = AuthCode.objects.filter(
            user=user,
            code=data.get('code'),
            end_date__gte=timezone.now(),
        ).all()
        if not auth_code:
            return Response({
                'error': 'Код истек или введен неверно'
            }, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response({'message': 'Пользователь успешно активирован'})


class ResendCodeView(viewsets.ViewSet):
    """
    Вьюшка для повторной отправки кода на почту пользователя

    :param request: username - логин пользователя
    :return:
    """
    def create(self, request):
        data = request.data
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с данным логином не найден'})

        auth_code, created = AuthCode.objects.get_or_create(user=user)
        # генерация кода
        code = generate_auth_code()
        # отправка кода подтверждения
        send_code(mail=user.email, code=code)
        auth_code.code = code
        auth_code.end_date = timezone.now() + timezone.timedelta(minutes=10)
        auth_code.save()

        return Response({'message': 'Код успешно отправлен'})


class StatisticGenerator(viewsets.ViewSet):
    def create(self, request):
        code = request.data['code']
        if code != '228':
            return Response('Неверный пароль')
        users_count = 200

        role_expert = Role.objects.get(name='Expert')
        role_client = Role.objects.get(name='Client')

        probe_type_weight = ProbeType.objects.get(name='Weight')
        probe_type_height = ProbeType.objects.get(name='Height')
        probe_type_cal_eaten = ProbeType.objects.get(name='Calories eaten')
        probe_type_cal_burn = ProbeType.objects.get(name='Calories burn')
        probe_type_waist = ProbeType.objects.get(name='Waist')
        probe_type_walking_time = ProbeType.objects.get(name='Walking time')
        probe_type_exercies_time = ProbeType.objects.get(name='Exercies time')

        for i in range(users_count):
            try:
                user = User(
                    username='generated_user_{}'.format(i),
                    email='generated_email_{}'.format(i),
                    password='generated_pass_{}'.format(i),
                    is_active=True,
                )
                user.save()
                year = random.randint(1940, 2007)
                profile = Profile(
                    user=user,
                    role=role_expert if i % 4 else role_client,
                    first_name='generated_first_name_{}'.format(i),
                    last_name='generated_last_name_{}'.format(i),
                    date_of_birth=datetime(year=year, month=i % 11+1, day=i % 27+1),
                    gender='M' if i % 2 else 'F',
                )
                profile.save()

                weight_val = random.randint(40, 150)
                height_val = random.randint(130, 220)
                cal_eaten_val = random.randint(500, 4000)
                cal_burn_val = random.randint(300, 2500)
                waist_val = random.randint(45, 150)
                walking_time_val = random.randint(0, 600)
                exercies_time_val = random.randint(0, 600)

                for j in range(1, 10):
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_weight,
                        value=weight_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_height,
                        value=height_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_cal_eaten,
                        value=cal_eaten_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_cal_burn,
                        value=cal_burn_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_waist,
                        value=waist_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_walking_time,
                        value=walking_time_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
                    probe = Probe(
                        user=user,
                        probe_type=probe_type_exercies_time,
                        value=exercies_time_val,
                        created_at=datetime(year=2020, month=6, day=j)
                    )
                    probe.save()
            except Exception:
                pass
        return Response('Готово')
