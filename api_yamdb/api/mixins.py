from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ListCreateDeleteViewSet(GenericViewSet, CreateModelMixin,
                              DestroyModelMixin, ListModelMixin):
    """Кастомный базовый класс для жанров и категорий."""
    pass
