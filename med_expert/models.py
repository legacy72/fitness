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


    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
    )

    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=150,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        error_messages={'unique': 'Пользователь с таким email уже существует.'},
        null=True,
    )

    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
        null=True,
    )

    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )
    gender = models.CharField(
        verbose_name='Пол', 
        max_length=2, 
        choices=GENDER_CHOICES,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['username', 'first_name', 'last_name', 'middle_name']),
        ]


    def __str__(self):
        return self.username


class Expert(User):  
    rate = models.FloatField(
        verbose_name='Рейтинг',
    )

    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'


    def __str__(self):
        return super(User).username


class MedicalCenter(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=150,
    )

    address = models.CharField(
        verbose_name='Адрес',
        max_length=150,
    )

    rate = models.FloatField(
        verbose_name='Рейтинг',
    )

    description = models.TextField(
        verbose_name='Описание', 
        null=True,
    )

    class Meta:
        verbose_name = 'Медицинский центр'
        verbose_name_plural = 'Медицинские центры'
        indexes = [
            models.Index(fields=['name', ]),
        ]


class Service(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=150,
    )

    date_create = models.DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )

    date_provision = models.DateTimeField(
        verbose_name='Дата предоставления',
        default=timezone.now,
    )

    date_finish = models.DateTimeField(
        verbose_name='Дата окончания',
        default=timezone.now,
    )

    cost = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=30,
        decimal_places=2,
    )

    STATUS_CHOICES = (
        ('process', 'В процессе'),
        ('done', 'Выполнено'),
        ('cancel', 'Отменено'),
    )
    status = models.CharField(
        verbose_name='Статус заказа', 
        max_length=20, 
        choices=STATUS_CHOICES
    )

    medical_center = models.ForeignKey(
        MedicalCenter,
        verbose_name='Медицинское учреждение',
        on_delete=models.CASCADE,
    )
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


    def __str__(self):
        return self.name


class Consultation(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=150,
    )

    date_create = models.DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )

    date_provision = models.DateTimeField(
        verbose_name='Дата предоставления',
        default=timezone.now,
    )

    date_finish = models.DateTimeField(
        verbose_name='Дата окончания',
        default=timezone.now,
    )

    cost = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=30, 
        decimal_places=2,
    )

    STATUS_CHOICES = (
        ('process', 'В процессе'),
        ('done', 'Выполнено'),
        ('cancel', 'Отменено'),
    )
    status = models.CharField(
        verbose_name='Статус заказа', 
        max_length=20, 
        choices=STATUS_CHOICES
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='client',
    )

    expert = models.ForeignKey(
        Expert,
        verbose_name='Эксперт',
        on_delete=models.CASCADE,
        related_name='expert',
    )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'


    def __str__(self):
        return self.name
