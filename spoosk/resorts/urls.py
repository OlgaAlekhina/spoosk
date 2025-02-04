from django.urls import path
from .views import SkiResortList, SkiResortDetailView, Search, advanced_filter, get_review
from . import views

urlpatterns = [
    path('', SkiResortList.as_view(), name='resorts'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('filter/', advanced_filter, name='filter'),
    path('<slug>/', SkiResortDetailView.as_view(), name='resort_detail'),
    path('get_review/<str:pk>/', get_review, name='get_review'),
]