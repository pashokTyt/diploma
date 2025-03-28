import datetime as dt
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PublishedNPA, Region, Source
from django_filters import rest_framework as filters  # type: ignore
from . filter import NpaFilter
from rest_framework import filters
from django_filters import rest_framework as filters_dj
from . serializers import PublishedNpaSerializer, RegionSerializer, SourceSerializer
from .pagination import PublishedNpaPagination
from django.db.models import Count


from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Апишки диплома",
        default_version='v1',
        description="",
        terms_of_service="",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# вывод основных данных, есть фильтр и поиск по имени, пагинация готова
# надо больше логики делать, пока тут несерьезно все
# ****** больше почитать про миксины, генерик, орм

# select_related вот тут это юзать(быстрые и оптимизированные запросы к бд)
class PublishedNpaViewSet(GenericViewSet,
                          ListModelMixin,
                          RetrieveModelMixin
                          ):
    queryset = PublishedNPA.objects.all()
    serializer_class = PublishedNpaSerializer
    filterset_class = NpaFilter
    pagination_class = PublishedNpaPagination
    filter_backends = (filters_dj.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    @action(methods=['GET'], detail=False)
    def get_chart_data(self, request):
        today = dt.date.today() - dt.timedelta(weeks=0)
        dates = [(today - dt.timedelta(days=i)).strftime('%d-%m-%Y')
                 for i in range(7)]

        region_name = str(request.query_params.get(
            'region_name', None)).upper()

        filtered_queryset = self.queryset.filter(
            date_now__in=[dt.datetime.strptime(
                date, '%d-%m-%Y').date() for date in dates]
        )
        
        if region_name:
            filtered_queryset = filtered_queryset.filter(
                region__name__iexact=region_name)

        count_all_per_day = filtered_queryset.values(
            'date_now').annotate(count=Count('id'))
        """ categories_line = [item['date_now'] for item in count_all_per_day] """
        categories_line = []
        for item in count_all_per_day:
            categories_line.append(f'{item['date_now']}')

        series_line = [{'name': 'Опубликовано', 'data': [
            item['count'] for item in count_all_per_day]}]

        count_sources = filtered_queryset.filter(date_now=today).values(
            'source__name').annotate(count=Count('id'))
        categories_sources = [item['source__name'] for item in count_sources]
        series_sources = [{'name': 'Опубликовано', 'data': [
            item['count'] for item in count_sources]}]

        count_regions = filtered_queryset.values(
            'region__name').annotate(count=Count('id'))
        categories_regions = [item['region__name'] for item in count_regions]
        series_regions = [[
            item['count'] for item in count_regions]]

        data_to_serialize = {
            'count_all_per_day': {
                "categories": categories_line,
                "series": series_line
            },
            'count_sources': {
                "categories": categories_sources,
                "series": series_sources
            },
            'count_regions': {
                "labels": categories_regions,
                "series": series_regions
            },
        }

        return Response(data_to_serialize)


class SourceViewsSet(GenericViewSet,
                     ListModelMixin,):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class RegionViewSet(GenericViewSet,
                    ListModelMixin,):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
