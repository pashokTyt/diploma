from django_filters import rest_framework as filters  # type: ignore
from .models import PublishedNPA


class NpaFilter(filters.FilterSet):
    region_code = filters.CharFilter(
        field_name='region__code', lookup_expr='icontains', required=False)

    region_name = filters.CharFilter(
        field_name='region__name', lookup_expr='icontains', required=False)

    source_name = filters.CharFilter(
        field_name='source__name', lookup_expr='icontains', required=False)

    publish_date = filters.DateFromToRangeFilter(
        field_name='publish_date', required=False)

    write_date = filters.DateFromToRangeFilter(
        field_name='write_date', required=False)

    published = filters.BooleanFilter(field_name='published', required=True)

    class Meta:
        model = PublishedNPA
        fields = {
            'region__code': ['exact'],
            'source__name': ['exact'],
            'published': ['exact'],
        }
