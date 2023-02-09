from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import IsadminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=name',)


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=name',)


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