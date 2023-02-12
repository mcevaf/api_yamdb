from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


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
        validators=[
            MinValueValidator(1, 'Введите число от 1 до 10'),
            MaxValueValidator(10, 'Введите число от 1 до 10')],
        verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date')
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')]

    def __str__(self):
        return self.text[:15]



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
        ordering = ('-pub_date')

    def __str__(self):
        return self.text[:15]
