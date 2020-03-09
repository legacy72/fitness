from django.db import models
from django.contrib.auth.models import AbstractUser


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
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )

    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        error_messages={'unique': 'Пользователь с таким email уже существует.'},
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
        choices=GENDER_CHOICES
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['username', 'first_name', 'last_name', 'middle_name']),
        ]


    def __str__(self):
        return self.username
