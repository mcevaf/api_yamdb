from django_filters import CharFilter, FilterSet


class TitleFilter(FilterSet):
    """Фильтры для произведений."""
    genre = CharFilter('genre__slug')
    category = CharFilter('category__slug')
    name = CharFilter('name')
    year = CharFilter('year')
