from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .filters import ResortFilter
from .models import SkiResort, Month, RidingLevel


class Region:

    @staticmethod
    def get_regions():
        q = SkiResort.objects.values('region').distinct('region')
        b = [{'region': 'Все регионы'}]
        return b + list(q)

    @staticmethod
    def get_months():
        q = Month.objects.all()
        b = [{'name': 'Не важно'}]
        return b + list(q)

    @staticmethod
    def get_riding_level():
        q = RidingLevel.objects.all()
        b = [{'name': 'Не важно'}]
        return b + list(q)

    # def get_months_ski(self):
    #     q = SkiResort.objects.values('begin_season').distinct('begin_season')
    #     b = [{'begin_season': 'Не важно'}]
    #     return b + list(q)


class SkiResortList(Region, ListView):
    model = SkiResort
    template_name = 'resorts.html'
    context_object_name = 'resorts'

    def get_queryset(self):
        # return SkiResort.objects.order_by('name')
        return SkiResort.objects.order_by('name')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_length_calculation'] = SkiResort.total_length_calculation
        context['max_height_difference'] = SkiResort.max_height_difference
        context['count_trail'] = SkiResort.count_trail
        context['ski_pass_one'] = SkiResort.ski_pass_one
        context['count'] = SkiResort.count
        context['type_name_price'] = SkiResort.type_name_price

        # context['where'] = 'Все регионы'
        # context['when'] = 'Не важно'

        return context


class SkiResortDetailView(View):
    # model = SkiResort
    # template_name = 'resort_detail.html'
    # context_object_name = 'resort'
    # slug_field = "name"

    def get(self, request, slug):
        resort = SkiResort.objects.get(name=slug)
        return render(request, 'resort_detail.html', {"resort": resort})


class FilterResortsView(Region, ListView):
    queryset = SkiResort.objects.all()
    template_name = 'base_searching_results.html'
    context_object_name = 'resorts'

    @staticmethod
    def get_queryset_complexity(level):
        if level == 'Ученик':
            q = SkiResort.objects.filter(skytrail__complexity='green').distinct('name')
        elif level == 'Новичок':
            q = SkiResort.objects.filter(skytrail__complexity='blue').distinct('name')
        elif level == 'Опытный':
            q = SkiResort.objects.filter(skytrail__complexity='red').distinct('name')
        elif level == 'Экстремал':
            q = SkiResort.objects.filter(skytrail__complexity='black').distinct('name')
        else:
            q = SkiResort.objects.all()

        return q

    def get_queryset(self):
        # queryset = super().queryset
        where = self.request.GET.get('where')
        when = self.request.GET.get('when')
        riding_level = self.request.GET.get('riding_level')

        qs1 = SkiResort.objects.filter(region__icontains=where).distinct('name')
        # self.filterset = ResortFilter({'region': f1}, queryset=queryset).qs
        qs2 = SkiResort.objects.filter(list_month__icontains=when).distinct('name')
        qs3 = self.get_queryset_complexity(riding_level)


        if where == '':
            where = 'Все регионы'
        if when == '':
            when = 'Не важно'
        if riding_level == '':
            riding_level = 'Не важно'

        if where == 'Все регионы':
            if when == 'Не важно' and riding_level == 'Не важно':
                self.filterset = SkiResort.objects.all()
            elif when != 'Не важно' and riding_level == 'Не важно':
                self.filterset = qs2
            elif when == 'Не важно' and riding_level != 'Не важно':
                self.filterset = qs3
            elif when != 'Не важно' and riding_level != 'Не важно':
                self.filterset = qs2 & qs3

        else:
            if when == 'Не важно' and riding_level == 'Не важно':
                self.filterset = qs1
            elif when != 'Не важно' and riding_level == 'Не важно':
                self.filterset = qs1 & qs2
            elif when == 'Не важно' and riding_level != 'Не важно':
                self.filterset = qs1 & qs3
            elif when != 'Не важно' and riding_level != 'Не важно':
                self.filterset = qs2 & qs3 & qs1

        return self.filterset



        # if where == 'Все регионы' and when == 'Не важно' and riding_level == 'Не важно':
        #     self.filterset = SkiResort.objects.all()
        # if where != 'Все регионы' and when == 'Не важно' and riding_level == 'Не важно':
        #     self.filterset = qs1
        # if where == 'Все регионы' and when != 'Не важно' and riding_level == 'Не важно':
        #     self.filterset = qs2
        # if where == 'Все регионы' and when == 'Не важно' and riding_level != 'Не важно':
        #     self.filterset = qs3
        # if where != 'Все регионы' and when != 'Не важно' and riding_level == 'Не важно':
        #     self.filterset = qs1 & qs2
        # if where != 'Все регионы' and when == 'Не важно' and riding_level != 'Не важно':
        #     self.filterset = qs1 & qs3
        # if where == 'Все регионы' and when != 'Не важно' and riding_level != 'Не важно':
        #     self.filterset = qs2 & qs3
        # if where != 'Все регионы' and when != 'Не важно' and riding_level != 'Не важно':
        #     self.filterset = qs2 & qs3 & qs1
        # return self.filterset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # where = self.request.GET.get('where')
        # when = self.request.GET.get('when')
        # context['where'] = where
        # context['when'] = when

        where = self.request.GET.get('where')
        context['where'] = where

        when = self.request.GET.get('when')
        context['when'] = when

        riding_level = self.request.GET.get('riding_level')
        context['riding_level'] = riding_level

        # context['filter'] = self.filterset.qs

        context['resorts_length'] = len(self.filterset)
        return context


# class FilterResortsView1(Region, ListView):
#     queryset = SkiResort.objects.all()
#     template_name = 'base_searching_results.html'
#     context_object_name = 'resorts'
#
# def get_queryset(self): queryset = SkiResort.objects.filter(region__in=self.request.GET.getlist("region"),
# begin_season__in=self.request.GET.getlist("month")) return queryset

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     # context['form'] = self.filterset.form
#     # where = ResortFilter(self.request.GET.get('where'))
#     # context['where'] = where
#     region = self.request.GET.get('region')
#     context['region'] = region
#     begin_season = self.request.GET.get('begin_season')
#     context['begin_season'] = begin_season
#     context['resorts_length'] = len(self.filterset.qs)
#     return context

# class SearchingResultsList(Region, ListView):
#     model = SkiResort
#     template_name = 'searching_results.html'
#     context_object_name = 'resorts'
#
#     def get_queryset(self):
#         # queryset = SkiResort.objects.filter('region__in' == self.request.GET.getlist("region"))
#         queryset = SkiResort.objects.filter('region__in' == self.request.GET.get('where', ''))
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_length_calculation'] = SkiResort.total_length_calculation
#         context['max_height_difference'] = SkiResort.max_height_difference
#         context['count_trail'] = SkiResort.count_trail
#         context['ski_pass_one'] = SkiResort.ski_pass_one
#
#         return context
