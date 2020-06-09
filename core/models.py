from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now as now_local
from django.utils import timezone


class User(AbstractUser):
    password_hash = models.CharField(
        verbose_name='Хэш пароля',
        max_length=250,
        null=True,
        blank=True,
    )

    password_salt = models.CharField(
        verbose_name='Соль пароля',
        max_length=250,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=150,
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    img = models.TextField(
        verbose_name='Картинка',
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )

    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
    )

    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )
    gender = models.CharField(
        verbose_name='Пол',
        max_length=2,
        choices=GENDER_CHOICES,
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        indexes = [
            models.Index(fields=['last_name']),
        ]

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class Chat(models.Model):
    members = models.ManyToManyField(User, verbose_name='Участник')

    created_at = models.DateTimeField(
        'Время создания',
        default=now_local,
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class MemberShip(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    permissions = models.CharField(
        verbose_name='Разрешения',
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Членство'
        verbose_name_plural = 'Членства'


class ProbeType(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=150,
    )

    input_method = models.IntegerField(
        verbose_name='Метод ввода'
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тип замера'
        verbose_name_plural = 'Типы замеров'

    def __str__(self):
        return self.name


class Probe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    probe_type = models.ForeignKey(ProbeType, on_delete=models.CASCADE)

    value = models.CharField(
        verbose_name='Значение',
        max_length=250,
    )

    created_at = models.DateTimeField(
        'Время создания',
        default=now_local,
    )

    class Meta:
        verbose_name = 'Замер'
        verbose_name_plural = 'Замеры'


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)

    text = models.TextField(
        verbose_name='Текст',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        'Время создания',
        default=now_local,
    )

    is_read = models.BooleanField(verbose_name='Прочитано', default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return self.text


class AuthCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(verbose_name='Код', max_length=255)
    start_date = models.DateTimeField(verbose_name='Дата генерации', auto_now=True)
    end_date = models.DateTimeField(
        verbose_name='Дата окончания действия',
        default=timezone.now() + timedelta(minutes=10)
    )

    class Meta:
        verbose_name = 'Код'
        verbose_name_plural = 'Коды'
