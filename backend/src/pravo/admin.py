from django.contrib import admin
from .models import Region, Source, PublishedNPA
# Register your models here.


@admin.register(PublishedNPA)
class PublishedNPAAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'published',
                    'name',
                    'number',
                    'publish_date',
                    'write_date',
                    'date_now',
                    'link_to_download',
                    'source__name',
                    'region__name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'code'
    ]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'url_address'
    ]
