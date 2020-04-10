from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={'unique': 'Пользователь с таким логином уже существует.'},
    )

    password_hash = models.CharField(
        verbose_name='Хэш пароля',
        max_length=250,
    )

    password_salt = models.CharField(
        verbose_name='Соль пароля',
        max_length=250,
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.OneToOneField(Role, on_delete=models.CASCADE)

    img = models.CharField(
        verbose_name='Картинка',
        max_length=250,
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
    created_at = models.DateTimeField(
        'Время создания',
        default=timezone.now(),
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
    # TODO: permissions должны быть таблицей, а костян питух
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

    # TODO: input_method должен быть чойсами, а костян питух
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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    probe_type = models.ForeignKey(ProbeType, on_delete=models.CASCADE)

    value = models.CharField(
        verbose_name='Значение',
        max_length=250,
    )

    created_at = models.DateTimeField(
        'Время создания',
        default=timezone.now(),
    )

    class Meta:
        verbose_name = 'Замер'
        verbose_name_plural = 'Замеры'


class Message(models.Model):
    member_ship = models.ForeignKey(MemberShip, on_delete=models.CASCADE)

    created_at = models.DateTimeField(
        'Время создания',
        default=timezone.now(),
    )

    text = models.TextField(
        verbose_name='Текст',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
