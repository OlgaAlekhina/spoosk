import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .filters import MainFilter
from .forms import SkiReviewForm, ReviewImageForm
from .models import SkiResort, Month, RidingLevel, SkiReview, ReviewImage, SkiPass, SkyTrail
from django.db.models import OuterRef, Subquery, FloatField, Avg
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required


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
    filter_results = MainFilter(data).qs.annotate(rating=Coalesce(Subquery(ratings), 0, output_field=FloatField())).order_by('-rating', 'name')
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
        return SkiResort.objects.annotate(rating=Coalesce(Subquery(ratings), 0, output_field=FloatField())).order_by('-rating', 'name')[:6]

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


def autocomplete(request):
    if 'term' in request.GET:
        qs = SkiResort.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for resort in qs:
            names.append(resort.name)
        return JsonResponse(names, safe=False, json_dumps_params={'ensure_ascii': False})


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
