from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year

ROLE_CHOICES = [
    (settings.ADMIN, 'администратор'),
    (settings.MODERATOR, 'модератор'),
    (settings.USER, 'пользователь')
]


class User(AbstractUser):
    '''AbstractUser - раcширенная модель пользователя(user)'''
    username = models.CharField(
        'Имя пользователя',
        validators=(validate_username,),
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Email',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=max((len(item) for _, item in ROLE_CHOICES)),
        choices=ROLE_CHOICES,
        default=settings.USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=settings.USERNAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=settings.USERNAME_MAX_LENGTH,
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
        null=True,
        blank=False,
    )

    '''Декоратор @property возвращает из метода класса в атрибут класса'''
    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR or self.is_staff

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class AbstractCategoryGenre(models.Model):
    """Абстрактная модель для категорий и жанров."""
    name = models.CharField(
        'Наименование',
        max_length=settings.GENRE_CATEGORY_TITLE_MAX_LENGTH)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        abstract = True
        ordering = ('name', 'slug',)

    def __str__(self):
        return self.slug


class Category(AbstractCategoryGenre):
    """Модель для категорий."""

    class Meta(AbstractCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractCategoryGenre):
    """Модель для жанров."""

    class Meta(AbstractCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(
        'Наименование произведения',
        max_length=settings.GENRE_CATEGORY_TITLE_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(validate_year,),
        db_index=True)
    description = models.TextField('Описание',)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная таблица связи жанров и произведений"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение-жанр'
        verbose_name_plural = 'Произведения-Жанры'

    def __str__(self):
        return f'{self.title}: {self.genre}'


class AbstractReviewComment(models.Model):
    """Абстрактная модель для отзывов и комментариев."""
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)
    text = models.TextField('Текст',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.REVIEW_COMMENT_STR_LENGTH]


class Review(AbstractReviewComment):
    """Модель для отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Отзыв')
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(1, 'Введите число от 1 до 10'),
            MaxValueValidator(10, 'Введите число от 1 до 10')],
        default=1)

    class Meta(AbstractReviewComment.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')]


class Comment(AbstractReviewComment):
    """Модель для комментарий."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв')

    class Meta(AbstractReviewComment.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
