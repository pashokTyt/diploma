# делаем api, возвращающий данные
from django.contrib import admin  # type: ignore
from django.urls import path, include, re_path  # type: ignore
from pravo import views
from rest_framework import routers  # type: ignore


router = routers.DefaultRouter()
router.register(r'published-npa', views.PublishedNpaViewSet,
                basename='published-npa')
router.register(r'regions', views.RegionViewSet, basename='regions')
router.register(r'sources', views.SourceViewsSet, basename='sources')


urlpatterns = [
    # swagger
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', views.schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', views.schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    # swagger ends


    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
