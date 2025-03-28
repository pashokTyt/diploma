from rest_framework import serializers  # type: ignore
from .models import Region, Source, PublishedNPA
# тут можно еще валидировать данные, на заметочку


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['name', 'url_address']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['name', 'code']

# все данные по 1 странице(таблица)


class PublishedNpaSerializer(serializers.ModelSerializer):
    #  почитать про  prefetch_related, вроде тут пригодится
    source = SourceSerializer()
    region = RegionSerializer()

    class Meta:
        model = PublishedNPA
        fields = '__all__'
