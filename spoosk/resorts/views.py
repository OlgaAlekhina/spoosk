import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from rest_framework import status
from .filters import MainFilter
from .forms import SkiReviewForm, ReviewImageForm
from .models import SkiResort, Month, RidingLevel, SkiReview, ReviewImage, SkiPass, SkyTrail
from .serializers import SkiResortSerializer, ResortSerializer, SkireviewSerializer, SkireviewUpdateSerializer
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery, IntegerField, Exists, FloatField, Prefetch, Sum, Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.decorators import action
from django.db.models.functions import Coalesce
from spoosk.permissions import AuthorEditOrReadOnly, APIkey
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required


# endpoints for resorts
class SkiResortViewset(viewsets.ReadOnlyModelViewSet):
    """
    list: Выводится список всех курортов - по 7 курортов на страницу. Запрос может включать номер страницы в качестве параметра. Пример: /api/resorts/?page=2
    В теле ответа передаются параметры next и previous, которые содержат ссылки на предыдущую и следующую страницы, и параметр account, содержащий общее количество найденных объектов.
    Этот эндпоинт также можно использовать для поисковой строки. Для этого передается параметр search после вопросительного знака. Значением параметра служит текст, который пользователь ввел в поисковую строку.
    Пример: /api/resorts/?search=газпром
    Поиск осуществляется по названию курорта.
    Условия доступа к эндпоинту: APIkey

    retrieve: Выводит все данные о курорте по его id.
              Условия доступа к эндпоинту: APIkey

    reviews: Список всех отзывов для конкретного курорта, полученный по его id. Выводится по 7 отзывов на страницу, отсортированных по дате.
    Для получения других страниц в запросе надо передать номер страницы: /api/resorts/Gazprom/reviews/?page=2
    Условия доступа к эндпоинту: APIkey
    """
    permission_classes = [APIkey]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        ratings = SkiReview.objects.filter(resort=OuterRef("pk"), approved=True).order_by().values('resort').annotate(
            resort_rating=Avg('rating', output_field=FloatField())).values('resort_rating')[:1]
        queryset = SkiResort.objects.prefetch_related(
            Prefetch(
                # get skipass objects which have mobile type
                'resorts', queryset=SkiPass.objects.exclude(mob_type__isnull=True)
            )
        ).prefetch_related(
            Prefetch(
                # get skireview objects which have been approved
                'resort_reviews', queryset=SkiReview.objects.filter(approved=True)
            )
        ).annotate(rating=Coalesce(Subquery(ratings), 0, output_field=FloatField())).order_by('-rating')
        if user.is_authenticated:
            queryset = queryset.annotate(in_favorites=Exists(SkiResort.objects.filter(id_resort=OuterRef("pk"), users=user)))
        return queryset

    # add different serializers to different actions
    def get_serializer_class(self):
        if self.action == 'list':
            return ResortSerializer
        if self.action == 'retrieve':
            return SkiResortSerializer
        if self.action == 'reviews':
            return SkireviewSerializer

    def retrieve(self, request, pk=None):
        resort = SkiResort.objects.prefetch_related(
            Prefetch(
                # get skipass objects which have mobile type
                'resorts', queryset=SkiPass.objects.exclude(mob_type__isnull=True)
            )
        ).filter(id_resort=pk)
        if resort.exists():
            user = self.request.user
            if user.is_authenticated:
                resort = resort.annotate(in_favorites=Exists(SkiResort.objects.filter(id_resort=OuterRef("pk"), users=user)))
        else:
            return Response(dict(message='Resort not found.'),
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(resort[0])
        return Response(serializer.data)

    @action(detail=True)
    def reviews(self, request, pk=None):
        resort = self.get_object()
        reviews = resort.resort_reviews.all().order_by('-add_at')
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)


# endpoint for list of regions
@api_view()
@permission_classes([APIkey])
def get_regions(request):
    """ Выводит список всех регионов горнолыжных курортов, которые имеются в базе данных.
        Условия доступа к эндпоинту: APIkey
    """
    regions = SkiResort.objects.values('region').distinct('region')
    return Response(regions)


# endpoint for main resorts filter
class ResortMainFilter(generics.ListAPIView):
    """
    Этот фильтр может использоваться с сортировкой результатов или без.
    Необходимо передавать параметры, которые указал пользователь, после url и вопросительного знака.
    Значение параметра resort_region должно быть идентично названию региона в БД. Точные названия можно получить в эндпоинте /api/resorts/regions.
    Значение параметра resort_month – это название месяца (по-русски, можно с большой или маленькой буквы).
    Значение параметра resort_level может быть green, blue, red или black, что соответствует сложностям трасс курорта.
    Возможные значения остальных параметров указаны в описании каждого параметра в Swagger.
    Параметры resort_region, resort_month и resort_level могут иметь несколько значений, в этом случае их надо указывать через запятую без пробела.
    Если пользователь не выбрал никакого значения, то параметр в запросе передавать не нужно.
    Пример: /api/resorts/filter?resort_region=Алтай&resort_month=январь&resort_level=red&have_red_skitrails=red&have_gondola=1&airport_distance=100&ordering=skipass
    Такой запрос вернет все курорты в регионе Алтай с возможностью катания в январе на сложных трассах (для опытных туристов), в которых имеются трассы повышенной сложности, гондольные подъемники, и с расположением не далее 100 км от аэропорта. Курорты будут отсортированы по цене дневного скипасса (по возрастанию цены).
    Сортировка может осуществляться по протяженности трасс, по цене дневного скипасса и по рейтингу. Для этого указывается параметр ordering, который может иметь следующие значения: 1) trail_length (сортировка в порядке возрастания) или -trail_length (в порядке убывания); 2) skipass (в порядке возрастания) или -skipass (в порядке убывания); 3) rating (в порядке возрастания) или -rating (в порядке убывания).
    Выводится по 7 курортов на страницу. Запрос может включать номер страницы в качестве параметра.
    В теле ответа передаются параметры next и previous, которые содержат ссылки на предыдущую и следующую страницы, и параметр account, содержащий общее количество найденных объектов.
    Условия доступа к эндпоинту: APIkey
    """
    serializer_class = ResortSerializer
    filterset_class = MainFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = 'name'
    permission_classes = [APIkey]
    # pagination_class = None

    def get_queryset(self):
        user = self.request.user
        # annotation of queryset with trails number, rating and skipass price for ordering of the filtration result
        skipasses = SkiPass.objects.filter(id_resort=OuterRef("pk")).filter(mob_type="one_day")
        skitrails = SkyTrail.objects.filter(id_resort=OuterRef("pk")).order_by().values('id_resort').annotate(
            length=Sum('extent', output_field=IntegerField())).values('length')[:1]
        ratings = SkiReview.objects.filter(resort=OuterRef("pk"), approved=True).order_by().values('resort').annotate(
            resort_rating=Avg('rating', output_field=FloatField())).values('resort_rating')[:1]
        queryset = SkiResort.objects.annotate(trail_length=Coalesce(Subquery(skitrails), 0)). \
            annotate(skipass=Coalesce(Subquery(skipasses.values("price"), output_field=IntegerField()), 0)).annotate(
            rating=Coalesce(Subquery(ratings), 0, output_field=FloatField()))
        if user.is_authenticated:
            queryset = queryset.annotate(in_favorites=Exists(SkiResort.objects.filter(id_resort=OuterRef("pk"), users=user)))
        return queryset


# endpoints for reviews
class SkiReviewViewset(viewsets.ModelViewSet):
    """
    list: Выводит все последние отзывы на главный экран. Выводится по 7 отзывов на страницу, отсортированных по дате создания. Запрос может включать номер страницы в качестве параметра. Пример: /api/reviews/?page=2
          В теле ответа передаются параметры next и previous, которые содержат ссылки на предыдущую и следующую страницы, и параметр account, содержащий общее количество найденных объектов.
          Условия доступа к эндпоинту: APIkey
    retrieve: Выводит все данные отзыва по его id.
              Условия доступа к эндпоинту: APIkey
    create: Записывает новый отзыв в базу данных. Параметр images должен содержать список всех загруженных фото (в виде объектов файлов). Загрузка файлов в сваггере не работает, протестировать можно только в постмане.
            Условия доступа к эндпоинту: APIkey, токен авторизации
    partial_update: Осуществляет частичное редактирование отзыва по его id. Передавать можно только те параметры, которые подлежат изменению.
                    Параметр images должен содержать список вновь загруженных фото (в виде объектов файлов). Загрузка файлов в сваггере не работает, протестировать можно только в постмане.
                    Параметр deleted_images должен содержать список id (целые числа) фотографий, которые пользователь решил удалить при редактировании отзыва.
                    Условия доступа к эндпоинту: APIkey, токен авторизации (пользователь может редактировать только свои собственные отзывы)
    delete: Удаляет отзыв из базы данных по его id.
            Условия доступа к эндпоинту: APIkey, токен авторизации (пользователь может удалять только свои собственные отзывы)
    """
    permission_classes = [APIkey, AuthorEditOrReadOnly]
    queryset = SkiReview.objects.all()
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']]
    parser_classes = (JSONParser, MultiPartParser)

    # add different serializers to different actions
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SkireviewUpdateSerializer
        else:
            return SkireviewSerializer

    def list(self, request):
        items = SkiReview.objects.filter(approved=True).exclude(text='').order_by('-add_at')
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request, })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def partial_update(self, request, pk=None):
        review = self.get_object()
        if review.approved:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Отзыв нельзя редактировать после размещения на сайте",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            review.text = serializer.validated_data.get('text', review.text)
            review.rating = serializer.validated_data.get('rating', review.rating)
            review.save()
            image_number = len(review.review_images.all())
            deleted_images = serializer.validated_data.get('deleted_images', [])
            del_number = 0
            for num in deleted_images:
                image = ReviewImage.objects.filter(id=num, review=review).first()
                if image:
                    image.delete()
                    del_number += 1
            image_number = image_number - del_number
            images = request.FILES.getlist('images')
            list_images = list(images)
            review_images = []
            for index, image in enumerate(list_images):
                im = ReviewImage(review=review, image=image)
                im.save()
                review_images.append(im.image.url)
                if index == 9 - image_number:
                    break
            response = {
                "message": "Отзыв успешно обновлен",
                "data": serializer.validated_data,
                "added_images": review_images
                }
            return Response(response)
        return Response(serializer.errors)


# endpoint for adding resort to user's favorites or removing it
@api_view()
@permission_classes([APIkey, IsAuthenticated])
def favorites(request, id_resort):
    """
        Проверяет, есть ли курорт в избранном у пользователя и в зависимости от результата добавляет его в избранное или удаляет оттуда.
        Параметр id соответствует идентификатору курорта, пользователь определяется автоматически.
        Условия доступа к эндпоинту: APIkey, токен авторизации
    """
    resort = SkiResort.objects.filter(id_resort=id_resort).first()
    if resort:
        user = request.user
        if resort in SkiResort.objects.filter(users=user):
            resort.users.remove(user)
            message = 'Successfully delete resort from favorites!'
        else:
            resort.users.add(user)
            message = 'Successfully add resort to favorites!'
    else:
        message = 'Resort does not exist'
    return Response(message)


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
    easy = True if 'have_green_skitrails' in data else False
    medium = True if 'have_blue_skitrails' in data else False
    complex = True if 'have_red_skitrails' in data else False
    difficult = True if 'have_black_skitrails' in data else False
    freeride = True if 'have_freeride' in data else False
    snowpark = True if 'have_snowpark' in data else False
    bugel = True if 'have_bugelny' in data else False
    chair = True if 'have_armchair' in data else False
    gondola = True if 'have_gondola' in data else False
    travelator = True if 'have_travelators' in data else False
    adult = True if 'have_adult_school' in data else False
    if 'airport_distance' in data:
        distance = 0 if data.get('airport_distance') == '50' else 100
    else:
        distance = 200
    child = True if 'have_children_school' in data else False
    rental = True if 'have_rental' in data else False
    evening = True if 'have_evening_skiing' in data else False
    ratings = SkiReview.objects.filter(resort=OuterRef("pk"), approved=True).order_by().values('resort').annotate(
        resort_rating=Avg('rating', output_field=FloatField())).values('resort_rating')[:1]
    filter_results = MainFilter(data).qs.annotate(rating=Coalesce(Subquery(ratings), 0, output_field=FloatField())).order_by('-rating')
    html = render_to_string('base_searching_results2.html', context={'easy': easy, 'medium': medium, 'complex': complex, 'difficult': difficult, 'freeride': freeride,
                                                                     'snowpark': snowpark, 'bugel': bugel, 'chair': chair, 'gondola': gondola, 'travelator': travelator,
                                                                     'adult': adult, 'child': child, 'rental': rental, 'evening': evening, 'distance': distance,
                                                                     'resorts': filter_results, 'resorts_length': len(filter_results)}, request=request)
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
        ratings = SkiReview.objects.filter(resort=OuterRef("pk"), approved=True).order_by().values('resort').annotate(
            resort_rating=Avg('rating', output_field=FloatField())).values('resort_rating')[:1]
        return SkiResort.objects.annotate(rating=Coalesce(Subquery(ratings), 0, output_field=FloatField())).order_by('-rating').order_by('name')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_length_calculation'] = SkiResort.total_length_calculation
        context['max_height_difference'] = SkiResort.max_height_difference
        context['count_trail'] = SkiResort.count_trail
        context['skipass_min'] = SkiResort.skipass_min
        context['count'] = SkiResort.count
        context['type_name_price'] = SkiResort.type_name_price
        context['reviews'] = SkiReview.objects.filter(approved=True).order_by('-add_at')[:10]

        return context


class SkiResortDetailView(View):

    def get(self, request, slug):
        resort = SkiResort.objects.get(name=slug)
        reviews_list = SkiReview.objects.filter(resort=resort, approved=True).order_by('-add_at')
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


# get review data in modal
def get_review(request, pk):
    review = SkiReview.objects.get(id=pk)
    images_list = ReviewImage.objects.filter(review=review)
    images = []
    for im in images_list:
        img = {}
        img['id'] = im.id
        img['url'] = im.image.url
        images.append(img)
    author = review.author
    review_date = review.add_at.strftime("%d.%m.%Y")
    try:
        author_avatar = author.userprofile.avatar.url
    except:
        author_avatar = ''
    if author.first_name == '':
        author_name = author.userprofile.name
    else:
        if author.last_name != '':
            last_name = author.last_name[:1] + '.'
            author_name = author.first_name + ' ' + last_name
        else:
            author_name = author.first_name
    response_data = {}
    response_data['resort_name'] = review.resort.name
    response_data['review_id'] = pk
    response_data['resort_region'] = review.resort.region
    response_data['resort_url'] = review.resort.get_absolute_url()
    response_data['author_name'] = author_name
    response_data['author_avatar'] = author_avatar
    response_data['review_text'] = review.text
    response_data['review_rating'] = review.rating
    response_data['review_images'] = images
    response_data['review_data_at'] = review_date
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )
