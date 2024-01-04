import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .filters import ResortFilter, MainFilter
from .forms import SkiReviewForm, ReviewImageForm
from .models import SkiResort, Month, RidingLevel, SkiReview, ReviewImage
from django.http import JsonResponse
from .serializers import SkiResortSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string


class SkiResortViewset(viewsets.ReadOnlyModelViewSet):
   queryset = SkiResort.objects.all()
   serializer_class = SkiResortSerializer

   def get(self, request):
       items = SkiResort.objects.all()
       serializer = SkiResortSerializer(items, many=True)
       return Response(serializer.data)


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


# endpoint for advanced filter request
def advanced_filter(request):
    data = request.GET
    filter_results = MainFilter(data).qs
    html = render_to_string('base_searching_results2.html', context={'resorts': filter_results, 'resorts_length': len(filter_results)}, request=request)
    return JsonResponse(html, safe=False)


# endpoint for review form submit
def review_submit(request):
    if request.method == 'POST':
        id_resort = request.POST.get('id_resort')
        resort = SkiResort.objects.get(id_resort=id_resort)
        author = request.user
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        images = request.FILES.getlist('images')
        review = SkiReview.objects.create(resort=resort, author=author, rating=rating, text=text)
        for image in images:
            ReviewImage.objects.create(image=image, review=review)
        return JsonResponse({"success": "Add new review"}, status=200)
    else:
        raise Http404


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
        context['reviews'] = SkiReview.objects.all().order_by('-add_at')[:10]

        # context['where'] = 'Все регионы'
        # context['when'] = 'Не важно'

        return context


class SkiResortDetailView(View):

    def get(self, request, slug):
        resort = SkiResort.objects.get(name=slug)
        reviews_list = SkiReview.objects.filter(resort=resort).order_by('-add_at')
        reviews = reviews_list

        initial_data = {'resort': resort.id_resort}
        review_form = SkiReviewForm(initial=initial_data, request=request)
        image_form = ReviewImageForm()
        return render(request, 'resort_detail.html', {"resort": resort, "reviews": reviews, "review_form": review_form, 'image_form': image_form})

    def post(self, request, slug):
        resort = SkiResort.objects.get(name=slug)
        review_form = SkiReviewForm(request.POST, request=request)
        image_form = ReviewImageForm(request.POST, request.FILES)

        if review_form.is_valid() and image_form.is_valid():
            review_instance = review_form.save(commit=False)
            review_instance.author = request.user
            review_instance.save()

            image_instances = []
            for image in request.FILES.getlist('photo'):
                image_instance = ReviewImage.objects.create(photo=image, review=review_instance)
                image_instances.append(image_instance)

            return redirect('resort_detail', slug=review_instance.resort.name)
        else:
            reviews = SkiReview.objects.filter(resort=resort)
            review_form = SkiReviewForm(initial={'resort': resort.id_resort}, request=request)
            image_form = ReviewImageForm()
            return render(request, 'resort_detail.html', {"resort": resort, "reviews": reviews, 'review_form': review_form, 'image_form': image_form})


# class FilterResortsView(Region, ListView):
#     queryset = SkiResort.objects.all()
#     template_name = 'base_searching_results.html'
#     context_object_name = 'resorts'
#
#     @staticmethod
#     def get_queryset_complexity(level):
#         if level == 'Ученик':
#             q = SkiResort.objects.filter(skytrail__complexity='green').distinct('name')
#         elif level == 'Новичок':
#             q = SkiResort.objects.filter(skytrail__complexity='blue').distinct('name')
#         elif level == 'Опытный':
#             q = SkiResort.objects.filter(skytrail__complexity='red').distinct('name')
#         elif level == 'Экстремал':
#             q = SkiResort.objects.filter(skytrail__complexity='black').distinct('name')
#         else:
#             q = SkiResort.objects.all()
#
#         return q
#
#     def get_queryset(self):
#         # queryset = super().queryset
#         where = self.request.GET.get('where')
#         when = self.request.GET.get('when')
#         riding_level = self.request.GET.get('riding_level')
#
#         qs1 = SkiResort.objects.filter(region__icontains=where).distinct('name')
#         # self.filterset = ResortFilter({'region': f1}, queryset=queryset).qs
#         qs2 = SkiResort.objects.filter(list_month__icontains=when).distinct('name')
#         qs3 = self.get_queryset_complexity(riding_level)
#
#
#         if where == '':
#             where = 'Все регионы'
#         if when == '':
#             when = 'Не важно'
#         if riding_level == '':
#             riding_level = 'Не важно'
#
#         if where == 'Все регионы':
#             if when == 'Не важно' and riding_level == 'Не важно':
#                 self.filterset = SkiResort.objects.all()
#             elif when != 'Не важно' and riding_level == 'Не важно':
#                 self.filterset = qs2
#             elif when == 'Не важно' and riding_level != 'Не важно':
#                 self.filterset = qs3
#             elif when != 'Не важно' and riding_level != 'Не важно':
#                 self.filterset = qs2 & qs3
#
#         else:
#             if when == 'Не важно' and riding_level == 'Не важно':
#                 self.filterset = qs1
#             elif when != 'Не важно' and riding_level == 'Не важно':
#                 self.filterset = qs1 & qs2
#             elif when == 'Не важно' and riding_level != 'Не важно':
#                 self.filterset = qs1 & qs3
#             elif when != 'Не важно' and riding_level != 'Не важно':
#                 self.filterset = qs2 & qs3 & qs1
#
#         return self.filterset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         where = self.request.GET.get('where')
#         context['where'] = where
#
#         when = self.request.GET.get('when')
#         context['when'] = when
#
#         riding_level = self.request.GET.get('riding_level')
#         context['riding_level'] = riding_level
#
#         # context['filter'] = self.filterset.qs
#
#         context['resorts_length'] = len(self.filterset)
#         return context


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


# add resort to user's favorites
@login_required
def add_resort(request, pk):
    resort = SkiResort.objects.get(id_resort=pk)
    user = request.user
    if resort in SkiResort.objects.filter(users=user):
        resort.users.remove(user)
        response_data = {}
        response_data['result'] = 'Successfully delete resort from favorites!'
        response_data['action'] = 'delete'
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        resort.users.add(user)
        response_data = {}
        response_data['result'] = 'Successfully add resort to favorites!'
        response_data['action'] = 'add'
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )



def get_review(request):
    if request.method == 'POST':
        review_id = request.POST.get('reviewId')
        review = SkiReview.objects.get(id=review_id)

        review_data = {
            'name': review.name,
            'text': review.text,
        }

        return JsonResponse({'review': review_data})

    return JsonResponse({}, status=400) # Возвращаем ошибку, если метод запроса не POST




