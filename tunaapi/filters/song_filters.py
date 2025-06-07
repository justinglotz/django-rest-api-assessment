import django_filters
from tunaapi.models import Song


class SongFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    album = django_filters.CharFilter(lookup_expr='icontains')
    min_length = django_filters.NumberFilter(
        field_name='length', lookup_expr='gte')
    max_length = django_filters.NumberFilter(
        field_name='length', lookup_expr='lte')

    class Meta:
        model = Song
        fields = ['title', 'album', 'min_length', 'max_length']
