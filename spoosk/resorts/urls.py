from django.urls import path
from .views import SkiResortList, FilterResortsView, SkiResortDetailView, Search, add_resort
from . import views

urlpatterns = [
    path('', SkiResortList.as_view(), name='resorts'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('base_searching_results/', FilterResortsView.as_view(), name='base_searching_results'),
    path('<slug>/', SkiResortDetailView.as_view(), name='resort_detail'),
    path('add_resort/<int:pk>/', add_resort, name='add_resort'),
]