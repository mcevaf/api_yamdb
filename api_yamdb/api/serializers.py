from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = SlugRelatedField(
        slug_field='username', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')


    def validate(self, data):
        author=self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if title.reviews.select_related('title').filter(author=author):
                raise ValidationError(
                    'Отзыв можно оставить только один раз!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с коментариями."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date')
        read_only_fields = ('review', 'author')
