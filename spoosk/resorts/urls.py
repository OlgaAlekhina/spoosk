from django.urls import path
from .views import SkiResortList, FilterResortsView, SkiResortDetailView

urlpatterns = [
    path('', SkiResortList.as_view(), name='resorts'),
    path('base_searching_results/', FilterResortsView.as_view(), name='base_searching_results'),
    path('<str:slug>/', SkiResortDetailView.as_view(), name='resort_detail'),
]