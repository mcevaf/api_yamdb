from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator

from .validators import validate_username
from api_yamdb.settings import ADMIN, MODERATOR, USER

ROLE_CHOICES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER)
]


class User(AbstractUser):
    '''AbstractUser - разширенная модель пользователя(user)'''
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='1111'
    )

    '''Декоратор @property возвращает из метода класса в атрибут класса'''
    @property
    def admin(self):
        return self.role == ADMIN

    @property
    def moderator(self):
        return self.role == MODERATOR

    @property
    def user(self):
        return self.role == USER

    class Meta:
        ordering = ('id')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


'''Здесь должна быть функция получения кода подтверждения'''


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass