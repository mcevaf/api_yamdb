from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsadminUserOrReadOnly


class ListCreateDeleteViewSet(GenericViewSet, CreateModelMixin,
                              DestroyModelMixin, ListModelMixin):
    """Кастомный базовый класс для жанров и категорий."""
    lookup_field = 'slug'
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=name',)
