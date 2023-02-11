from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from reviews.validators import validate_username
from api_yamdb.settings import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            validate_username,
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH
    )


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            validate_username
        ]
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор получения данных произведения."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg', None)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления произведения."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), many=False
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
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
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date')
