import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, viewsets

from .permissions import IsadminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title


class ListCreateDeleteViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                               mixins.ListModelMixin, mixins.DestroyModelMixin):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)


class TitleFilter(django_filters.FilterSet):
    """Фильтры для произведений."""
    genre = django_filters.CharFilter('genre__slug')
    category = django_filters.CharFilter('category__slug')
    name = django_filters.CharFilter('name')
    year = django_filters.CharFilter('year')


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer