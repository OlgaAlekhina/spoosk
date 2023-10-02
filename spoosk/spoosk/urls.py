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
from accounts.views import signup_endpoint, login_endpoint, signup_confirmation, reset_request, reset_confirmation, reset_endpoint
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from rest_framework import routers
from resorts import views

router = routers.DefaultRouter()
router.register(r'resorts', views.SkiResortViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('resorts/', include('resorts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', RedirectView.as_view(pattern_name='resorts', permanent=True)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup_endpoint/', signup_endpoint, name='signup_endpoint'),
    path('login_endpoint/', login_endpoint, name='login_endpoint'),
    path('signup_confirmation/<uidb64>/<token>', signup_confirmation, name='signup_confirmation'),
    path('reset_request/', reset_request, name='reset_request'),
    path('reset_confirmation/', reset_confirmation, name='reset_confirmation'),
    path('reset_endpoint/', reset_endpoint, name='reset_endpoint'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_IMAGE_URL, document_root=settings.STATIC_IMAGE_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
