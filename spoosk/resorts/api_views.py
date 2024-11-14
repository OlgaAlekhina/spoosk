from rest_framework import status
from .filters import MainFilter
from .models import SkiResort, SkiReview, ReviewImage, SkiPass, SkyTrail
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


# endpoint for getting a list of regions
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

