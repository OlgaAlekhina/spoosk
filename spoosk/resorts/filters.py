import calendar
from datetime import datetime
import locale
import django_filters
from django.db.models import Q
from django_filters import FilterSet, CharFilter, Filter
from .models import SkiResort
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class ListFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(',')
        qs = super().filter(qs, value_list)
        return qs


class MainFilter(filters.FilterSet):
    resort_region = ListFilter(field_name="region", lookup_expr='in', label="parameter values are identical to form choice fields names")
    resort_month = CharFilter(field_name='list_month', method='filter_list_month', label="parameter values are identical to form choice fields names")
    resort_level = ListFilter(field_name='skytrail__complexity', distinct=True, lookup_expr='in', label="parameter values should be 'green' for 'Ученик', \
                                            'blue' for 'Новичок', 'red' for 'Опытный', 'black' for 'Экстремал'")
    have_green_skitrails = django_filters.Filter(field_name='skytrail__complexity', distinct=True,
                                                 label="parameter value should be 'green' if 'easy trails' is checked")
    have_blue_skitrails = django_filters.Filter(field_name='skytrail__complexity', distinct=True,
                                                label="parameter value should be 'blue' if 'medium trails' is checked")
    have_red_skitrails = django_filters.Filter(field_name='skytrail__complexity', distinct=True,
                                               label="parameter value should be 'red' if 'difficult trails' is checked")
    have_black_skitrails = django_filters.Filter(field_name='skytrail__complexity', distinct=True,
                                                 label="parameter value should be 'black' if 'hard trails' is checked")
    have_freeride = django_filters.Filter(field_name='freeride', distinct=True,
                                          label="parameter value should be '1' if 'freeride' is checked")
    have_snowpark = django_filters.Filter(field_name='snowpark', distinct=True,
                                          label="parameter value should be '1' if 'snowpark' is checked")
    have_gondola = django_filters.Filter(field_name='skilifts__gondola', distinct=True,
                                         label="parameter value should be '1' if 'gondola skilift' is checked")
    have_armchair = django_filters.Filter(field_name='skilifts__armchair', distinct=True,
                                          label="parameter value should be '1' if 'armchair skilift' is checked")
    have_bugelny = django_filters.Filter(field_name='skilifts__bugelny', distinct=True,
                                         label="parameter value should be '1' if 'bugelny skilift' is checked")
    have_travelators = django_filters.Filter(field_name='skilifts__travelators', distinct=True,
                                             label="parameter value should be '1' if 'travelator skilift' is checked")
    have_adult_school = django_filters.Filter(field_name='school', distinct=True,
                                              label="parameter value should be '1' if 'adult school' is checked")
    have_children_school = django_filters.Filter(field_name='children_school', distinct=True,
                                                 label="parameter value should be '1' if 'children school' is checked")
    airport_distance = django_filters.Filter(field_name='distance_airport', lookup_expr='lte', distinct=True,
                                             label="parameter value should be '50' or '100' if 'not more than 50 km' or 'not more than 100 km' is checked")
    have_rental = django_filters.Filter(field_name='equip_rental', distinct=True,
                                        label="parameter value should be '1' if 'equipment rental' is checked")
    have_evening_skiing = django_filters.Filter(field_name='evening_skiing', distinct=True,
                                                label="parameter value should be '1' if 'evening skiing' is checked")

    class Meta:
        model = SkiResort
        fields = ('resort_region', 'resort_month', 'resort_level', 'have_green_skitrails', 'have_blue_skitrails', 'have_red_skitrails', 'have_black_skitrails', 'have_freeride',
                  'have_snowpark', 'have_bugelny', 'have_armchair', 'have_gondola', 'have_travelators', 'have_adult_school',
                  'have_children_school', 'airport_distance', 'have_rental', 'have_evening_skiing')

    def filter_list_month(self, queryset, name, value):
        if value is not None:
            value_list = value.split(',')
            q = Q()
            for val in value_list:
                q |= Q(list_month__icontains=val)
            qs = queryset.filter(q)
        return qs


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



