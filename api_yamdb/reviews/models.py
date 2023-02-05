import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField('Наименование категории', max_length=256)
    slug = models.SlugField('Slug категории', unique=True)
    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField('Наименование жанра', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)
    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField('Наименование произведения', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска', 
        validators=[MaxValueValidator(
            dt.datetime.now().year,
            'Год не может быть больше текущего!'
            )
        ]
    )
    description = models.TextField('Описание',)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)