"""
URL configuration for spoosk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from resorts.api_views import SkiResortViewset, SkiReviewViewset, ResortMainFilter, get_regions, favorites
from accounts.api_views import UserViewset
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Spoosk API",
        default_version='v1',),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'resorts', SkiResortViewset, basename='SkiResort')
router.register(r'reviews', SkiReviewViewset)
router.register(r'users', UserViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('accounts.urls')),
    path('resorts/', include('resorts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/resorts/filter', ResortMainFilter.as_view()),
    path('api/resorts/regions', get_regions),
    path('api/resorts/<str:id_resort>/add_to_favorites/', favorites),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_IMAGE_URL, document_root=settings.STATIC_IMAGE_ROOT)
