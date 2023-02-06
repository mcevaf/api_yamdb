import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


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
        ordering = ('id')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
# post_save


class Review(models.Model):
    """Модель для отзывов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв')
    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True)
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Введите число от 1 до 10'),
            MaxValueValidator(10, 'Введите число от 1 до 10')
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')]


class Comment(models.Model):
    """Модель для комментарий."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']