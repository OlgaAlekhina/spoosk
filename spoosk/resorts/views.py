import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .filters import ResortFilter, MainFilter, AdvancedFilter
# from .forms import ReviewForm
from .models import SkiResort, Month, RidingLevel, SkiPass
from django.http import JsonResponse
from .serializers import SkiResortSerializer, ResortSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Prefetch


# endpoints for resorts
class SkiResortViewset(viewsets.ReadOnlyModelViewSet):
    queryset = SkiResort.objects.prefetch_related(
        Prefetch(
        'resorts', queryset=SkiPass.objects.exclude(mob_type__isnull=True) # get skipass objects which have mobile type
        )
    )
    serializer_class = SkiResortSerializer

    def get(self, request):
       items = SkiResort.objects.all()
       serializer = SkiResortSerializer(items, many=True)
       return Response(serializer.data)

    # add different serializers to list and detail view
    def get_serializer_class(self):
        if self.action == 'list':
            return ResortSerializer
        if self.action == 'retrieve':
            return SkiResortSerializer


# endpoint for main resorts filter
class ResortMainFilter(generics.ListAPIView):
    queryset = SkiResort.objects.all()
    serializer_class = ResortSerializer
    filterset_class = MainFilter


# endpoint for advanced resorts filter
class ResortAdvancedFilter(generics.ListAPIView):
    queryset = SkiResort.objects.all()
    serializer_class = ResortSerializer
    filterset_class = AdvancedFilter


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
        # context['reviews'] = Review.objects.all().order_by('-id')[:10]

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
        # reviews_list = Review.objects.filter(resort=resort).order_by('-id')
        # reviews = reviews_list
        #
        # form = ReviewForm()
        # return render(request, 'resort_detail.html', {"resort": resort, "reviews": reviews, "form": form})

    # def post(self, request, slug):
    #     resort = SkiResort.objects.get(name=slug)
    #     form = Review(request.POST)
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.resort = resort
    #         review.save()
    #         return redirect('resort_detail', slug=slug)
    #     else:
    #         reviews = Review.objects.filter(resort=resort)
    #         return render(request, 'resort_detail.html', {"resort": resort, "reviews": reviews, "form": form})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        where = self.request.GET.get('where')
        context['where'] = where

        when = self.request.GET.get('when')
        context['when'] = when

        riding_level = self.request.GET.get('riding_level')
        context['riding_level'] = riding_level

        # context['filter'] = self.filterset.qs

        context['resorts_length'] = len(self.filterset)
        return context


# def autocomplete(request):
#     query = request.GET.get('search')
#     results = list()
#     if query:
#         # resorts = SkiResort.objects.filter(name__startswish=query)
#         resorts = SkiResort.objects.filter(name__icontains=query)
#         for resort in resorts:
#             results.append({
#                 'name': resort.name
#             })
#
#     return JsonResponse({
#         'status': True,
#         'results': results
#     }, json_dumps_params={'ensure_ascii': False})

# def autocomplete(request):
#     if 'term' in request.GET:
#         qs = SkiResort.objects.filter(name__icontains=request.GET.get('term'))
#         results = []
#         for resort in qs:
#             resort_json = {}
#             resort_json['name'] = resort.name
#             resort_json['url'] = resort.get_absolute_url()
#             results.append(resort_json)
#
#         return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})

def autocomplete(request):
    if 'term' in request.GET:
        qs = SkiResort.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for resort in qs:
            names.append(resort.name)
        # titles = [product.title for product in qs]
        return JsonResponse(names, safe=False, json_dumps_params={'ensure_ascii': False})
#     # return render(request, 'default.html')

# def productListAjax(request):
#     if 'term' in request.GET:
#         qs = SkiResort.objects.filter(name__icontains=request.GET.get('term'))
#         names = list()
#         for resort in qs:
#             names.append(resort.name)
#
#         return JsonResponse(names, safe=False, json_dumps_params={'ensure_ascii': False})
    # return render(request, 'default.html')

# def search(request):
#     query = request.GET.get('search')
#     resorts = SkiResort.objects.filter(name__icontains=query)
#
#     context = {
#         'resorts': resorts
#     }
#
#     return render(request, 'search.html', context)


# def autosuggest(request):
#     query_original = request.GET.get('search')
#     queryset = SkiResort.objects.filter(name__icontains=query_original)
#     mylist = []
#     mylist += [x.name for x in queryset]
#     return JsonResponse(mylist, safe=False)

class Search(ListView):
    """Поиск курортов"""
    model = SkiResort
    queryset = SkiResort.objects.all()
    template_name = 'search.html'
    context_object_name = 'resorts'

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = SkiResort.objects.filter(name__istartswith=query)
        return queryset


    # def get(self, request, slug):
    #     query = self.request.GET.get('search')
    #     queryset = SkiResort.objects.filter(name__icontains=query)
    #     return render(request, 'resort_detail.html', {"resorts": queryset})


    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['s'] = self.request.GET('search')
    #     return context

    # def get(self, request, slug):
    #     resort = SkiResort.objects.get(name=slug)
    #     return render(request, 'resort_detail.html', {"resort": resort})




    # model = SkiResort
    # template_name = 'resort_detail.html'
    # context_object_name = 'resort'
    # slug_field = "name"

    # def get(self, request, slug):
    #     resort = SkiResort.objects.get(name=slug)
    #     return render(request, 'resort_detail.html', {"resort": resort})