import calendar
from datetime import datetime
import locale
import django_filters
from django.db.models import Q
from django_filters import FilterSet, CharFilter, Filter
from .models import SkiResort
from django_filters import rest_framework as filters


class ResortSimpleFilter(filters.FilterSet):
    resort_region = CharFilter(field_name='region', lookup_expr='icontains')
    resort_month = CharFilter(field_name='list_month', lookup_expr='icontains')

    class Meta:
        model = SkiResort
        fields = ['resort_region', 'resort_month']


#
# def filter_by_month(month_name):
#     _, value = calendar.month_name.index(month_name), calendar.month_name.index(month_name)
#     # Конвертируем название месяца в его номер, используя модуль calendar
#
#     begin_queryset = Q(begin_season__month__lte=value) & Q(end_season__month__gte=value)
#     end_before_queryset = Q(end_season__month__lt=value) & Q(end_season__year__gte=datetime.now().year)
#     begin_after_queryset = Q(begin_season__month__gt=value) & Q(begin_season__year__lte=datetime.now().year)
#
#     # Формируем диапазоны начала и конца сезона в виде заданных запросов
#
#     return SkiResort.objects.filter(begin_queryset | end_before_queryset | begin_after_queryset)


class ResortFilter(FilterSet):
    # region = CharFilter(field_name='region', lookup_expr='icontains')
    # begin_season = CharFilter(field_name='begin_season', lookup_expr='icontains')
    # month = CharFilter(field_name='month', lookup_expr='icontains')
    month_range = django_filters.CharFilter(method='mon')

    # @staticmethod
    # def filter_by_month(queryset, name, value):
    #     value1 = datetime.strptime(value, '%B').month
    #     return queryset.filter(
    #         Q(begin_season__lte=datetime(2000, value1, 1)) &
    #         Q(end_season__gte=datetime(2000, value1, 1))
    #     )

    @staticmethod
    def mon(f2):
        return SkiResort.objects.filter(list_month__icontains=f2)

    # @staticmethod
    # def by_month(f2):
    #     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    #     value = list(calendar.month_name).index(f2)
    #
    #     # _, value = calendar.month_name.index(month_name), calendar.month_name.index(month_name)
    #     begin_queryset = Q(begin_season__month__lte=value) & Q(end_season__month__gte=value)
    #     end_before_queryset = Q(end_season__month__lt=value) & Q(end_season__year__gte=datetime.now().year)
    #     begin_after_queryset = Q(begin_season__month__gt=value) & Q(begin_season__year__lte=datetime.now().year)
    #
    #     return SkiResort.objects.filter(begin_queryset | end_before_queryset | begin_after_queryset)

    # def filter_by_month(self, value):
    #     _, value1 = calendar.value.index(value)
    #     # Конвертируем название месяца в его номер, используя модуль calendar
    #
    #     begin_queryset = Q(begin_season__month__lte=value1) & Q(end_season__month__gte=value1)
    #     end_before_queryset = Q(end_season__month__lt=value1) & Q(end_season__year__gte=datetime.now().year)
    #     begin_after_queryset = Q(begin_season__month__gt=value1) & Q(begin_season__year__lte=datetime.now().year)
    #
    #     # Формируем диапазоны начала и конца сезона в виде заданных запросов
    #
    #     return queryset.filter(begin_queryset | end_before_queryset | begin_after_queryset)

    class Meta:
        model = SkiResort

        fields = ('region', 'month_range')

        # fields = {
        #     'region': ['icontains'],
        #     'list_month': ['in'],
        # }


#
# class MonthFilter(Filter):
#     def filter(self, qs, value):
#         if value:
#             return qs.filter(
#                 Q(begin_season__lte=datetime(2000, value, 1)) &
#                 Q(end_season__gte=datetime(2000, value, 1))
#             )
#         return qs
#
#
# class ResortFilter(FilterSet):
#     list_month = MonthFilter(field_name='begin_season')
#
#     class Meta:
#         model = SkiResort
#         fields = ('region', 'list_month')



