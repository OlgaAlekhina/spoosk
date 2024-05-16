from decimal import Decimal
from itertools import product
from django.db import models
from django.db.models import Sum, Max, Count, Avg
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class SkiLifts(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=20)  # Field name made lowercase.
    id_resort = models.ForeignKey('SkiResort', models.DO_NOTHING, db_column='ID_resort')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=True, null=True)
    extent = models.IntegerField(blank=True, null=True)
    armchair = models.IntegerField(blank=True, null=True)
    bugelny = models.IntegerField(blank=True, null=True)
    gondola = models.IntegerField(blank=True, null=True)
    travelators = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ski_lifts'


class SkiPass(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=20)  # Field name made lowercase.
    id_resort = models.ForeignKey('SkiResort', models.DO_NOTHING, db_column='ID_resort', related_name='resorts')  # Field name made lowercase.
    type = models.CharField(max_length=200, blank=True, null=True)
    mob_type = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    adult = models.IntegerField(blank=True, null=True)
    childlike = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unified = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ski_pass'

    def __str__(self):
        return f'{self.id_resort} : {self.mob_type}'


class SkiResort(models.Model):
    id_resort = models.CharField(db_column='ID_resort', primary_key=True, max_length=20, help_text="avalable: 'Sheregesh', 'Roza_hutor', 'Gazprom', 'Elbrus', 'Dombay', 'Big_wood', 'Arkhyz'")  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    begin_season = models.CharField(max_length=50, blank=True, null=True, help_text="start of the ski season month")
    end_season = models.CharField(max_length=50, blank=True, null=True, help_text="end of the ski season month")
    freeride = models.IntegerField(blank=True, null=True, help_text="'1' if resort has freeride, '0' if has not")
    snowpark = models.IntegerField(blank=True, null=True, help_text="'1' if resort has snowpark, '0' if has not")
    evening_skiing = models.IntegerField(blank=True, null=True, help_text="'1' if resort has evening skiing, '0' if has not")
    school = models.IntegerField(blank=True, null=True, help_text="'1' if resort has ski school, '0' if has not")
    ind_training = models.IntegerField(blank=True, null=True, help_text="have no idea what's this field for")
    children_school = models.IntegerField(blank=True, null=True, help_text="'1' if resort has training school for children, '0' if has not")
    equip_rental = models.IntegerField(blank=True, null=True, help_text="'1' if resort has equipment rental, '0' if has not")
    distance_airport = models.IntegerField(blank=True, null=True, help_text="km from airport")
    distance_railway = models.IntegerField(blank=True, null=True, help_text="km from railway station")
    info = models.TextField(blank=True, null=True, help_text="resort description")
    image = models.ImageField(null=True, upload_to="resorts/mini", blank=True, help_text="url of small image for resort's card")
    list_month = models.TextField(blank=True, null=True, help_text="list of months which cover the ski season")
    link_ofsite = models.CharField(blank=True, null=True, help_text="url of resort's website")
    link_skipasses = models.CharField(blank=True, null=True, help_text="url of skipasses page on resort's website")
    link_map = models.CharField(blank=True, null=True, help_text="url of resort's map")
    resort_map = models.ImageField(null=True, upload_to="resorts/maps", blank=True, help_text="url of image for resort's map")
    main_resort_img = models.ImageField(upload_to="resorts/maxi", null=True, blank=True, help_text="url of large image for resort's page header")
    max_height = models.IntegerField(blank=True, null=True, help_text="maximum height of resort")
    users = models.ManyToManyField(User, blank=True, related_name='user')

    class Meta:
        managed = True
        db_table = 'ski_resort'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("resort_detail", kwargs={"slug": self.name})

    @property
    def total_length_calculation(self):
        total = self.skytrail_set.all().aggregate(Sum('extent', default=0))
        result = round(total['extent__sum']//1000)
        return result

    @property
    def max_height_difference(self):
        max_height = self.skytrail_set.all().aggregate(Max('height_difference', default=0))
        result = max_height['height_difference__max']
        return result

    @property
    def ski_pass_one(self):
        price_skipass = self.resorts.all().filter(unified=1).values('price')
        price_skipass_list = list(price_skipass)
        if len(price_skipass_list):
            result = price_skipass_list
        else:
            result = [{'price': Decimal('0')}]

        return result[0]

    # get skipass for resort's card in mob app (where unified=1 & has minimal price)
    @property
    def skipass_min(self):
        skipass = self.resorts.filter(unified=1).order_by('price').first()
        if skipass:
            skipass_min = skipass.price
        else:
            skipass_min = 0
        return skipass_min

    @property
    def count_trail_calculation(self):
        all_trail = self.skytrail_set.all()
        count_trail = sum([trail.complexity for trail in all_trail])
        return count_trail

    @property
    def count_trail(self):
        all_trail = self.skytrail_set.all().values_list('complexity').annotate(total=Count('complexity'))
        d = list(all_trail)
        k = ['green', 'blue', 'red', 'black']

        fruit_dictionary = dict()
        for color, item in product(k, d):
            if item[0] == color:
                fruit_dictionary[color] = item[1]

        return fruit_dictionary

    @property
    def count(self):
        all_trail = self.skilifts_set.all().aggregate(armchair=Sum('armchair', default=0), bugelny=Sum('bugelny', default=0), gondola=Sum('gondola', default=0), travelators=Sum('travelators', default=0))

        return all_trail

    @property
    def trail_number_count(self):
        trail_number = len(self.skytrail_set.all())
        return trail_number

    @property
    def type_name_price(self):
        all_trail = self.resorts.all().exclude(mob_type__isnull=True).values('type', 'name', 'price')
        return all_trail

    @property
    def number_green_trails(self):
        green_trails = self.skytrail_set.all().filter(complexity="green")
        return len(green_trails)

    @property
    def number_blue_trails(self):
        blue_trails = self.skytrail_set.all().filter(complexity="blue")
        return len(blue_trails)

    @property
    def number_red_trails(self):
        red_trails = self.skytrail_set.all().filter(complexity="red")
        return len(red_trails)

    @property
    def number_black_trails(self):
        black_trails = self.skytrail_set.all().filter(complexity="black")
        return len(black_trails)

    @property
    def number_gondola(self):
        number_gondola = self.skilifts_set.all().filter(gondola='1')
        return len(number_gondola)

    @property
    def number_armchair(self):
        number_armchair = self.skilifts_set.all().filter(armchair='1')
        return len(number_armchair)

    @property
    def number_travelators(self):
        number_travelators = self.skilifts_set.all().filter(travelators='1')
        return len(number_travelators)

    @property
    def number_bugelny(self):
        number_bugelny = self.skilifts_set.all().filter(bugelny='1')
        return len(number_bugelny)

    # count resort's rating from reviews table
    @property
    def resort_rating(self):
        if self.resort_reviews.exists():
            resort_rating = self.resort_reviews.filter(approved=True).aggregate(Avg('rating'))
            average_rating = resort_rating['rating__avg']
            if average_rating == 4.5:
                return 5
            elif average_rating == 2.5:
                return 3
            else:
                return round(average_rating)
        else:
            return 0

    @property
    def web_rating(self):
        if self.resort_reviews.exists():
            resort_rating = self.resort_reviews.filter(approved=True).aggregate(Avg('rating'))
            return round(resort_rating['rating__avg'], 1)
        else:
            return 0

    @property
    def reviews_count(self):
        number_reviews = self.resort_reviews.filter(approved=True)
        return len(number_reviews)

    @property
    def green_trails_circle(self):
        g_length = self.skytrail_set.all().filter(complexity="green").aggregate(green=Sum('extent', default=0))
        # total_length = self.skytrail_set.all().aggregate(total=Sum('extent'))
        # green = g_length['green'] * 100 / total_length['total']
        # return int(green)
        return int(g_length['green'])

    @property
    def blue_trails_circle(self):
        # green = self.green_trails_circle()
        b_length = self.skytrail_set.all().filter(complexity="blue").aggregate(blue=Sum('extent', default=0))
        # total_length = self.skytrail_set.all().aggregate(total=Sum('extent'))
        # blue = b_length['blue'] * 100 / total_length['total'] + green
        # return int(blue)
        return int(b_length['blue'])

    @property
    def black_trails_circle(self):
        b_length = self.skytrail_set.all().filter(complexity="black").aggregate(black=Sum('extent', default=0))
        # total_length = self.skytrail_set.all().aggregate(total=Sum('extent'))
        # black = b_length['black'] * 100 / total_length['total']
        # return int(100 - black)
        return int(b_length['black'])

    @property
    def red_trails_circle(self):
        r_length = self.skytrail_set.all().filter(complexity="red").aggregate(red=Sum('extent', default=0))
        # total_length = self.skytrail_set.all().aggregate(total=Sum('extent'))
        # black = b_length['black'] * 100 / total_length['total']
        # return int(100 - black)
        return int(r_length['red'])


class SkyTrail(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=20)  # Field name made lowercase.
    id_resort = models.ForeignKey(SkiResort, models.DO_NOTHING, db_column='ID_resort')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=True, null=True)
    complexity = models.CharField(max_length=5, blank=True, null=True)
    extent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height_difference = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sky_trail'

    def __str__(self):
        return f'{self.id} - {self.name} - {self.complexity} - {self.extent} - {self.height_difference}'


class ResortImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="resorts/extra")
    resort = models.ForeignKey(SkiResort, on_delete=models.CASCADE, related_name='resort_images')
    add_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Month(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'month'

    def __str__(self):
        return f'{self.name}'

    def count_m(self):
        m = Month.objects.filter(id__gte=1) & Month.objects.filter(id__lte=5)
        return m


class RidingLevel(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'riding_level'

    def __str__(self):
        return f'{self.name}'


class SkiReview(models.Model):
    resort = models.ForeignKey(SkiResort, on_delete=models.CASCADE, related_name='resort_reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000, blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    add_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.resort} # {self.id}'


class ReviewImage(models.Model):
    image = models.ImageField(upload_to="reviews")
    review = models.ForeignKey(SkiReview, on_delete=models.CASCADE, related_name='review_images')
    add_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review} : photo # {self.id}'


# python manage.py shell_plus --print-sql
#  from django.db.models import *

# q = SkyTrail.objects.filter(id_resort='Elbrus')
# q = SkyTrail.objects.filter(id_resort='Elbrus').aggregate(Sum('extent'))
# g = SkiResort.objects.annotate(tot=Sum('skytrail__extent'))
# g=SkyTrail.objects.all()
# vars(g[0])
# h = SkiResort.objects.all()
# vars(h[0])
# h[0].totalmax1
# h[0].total


# h = SkyTrail.objects.all()
# vars(h[0])
# h[0].totalmax1
# h[0].total

# h = SkiLifts.objects.filter(id_resort='Elbrus').aggregate(armchair=Sum('armchair'), bugelny=Sum('bugelny'), gondola=Sum('gondola'), travelators=Sum('travelators'))
# .annotate(s1=Sum('started'),s2=Sum('finished'))
# SkiPass.objects.filter(id_resort='Elbrus').values('type', 'name', 'price')


# q = SkyTrail.objects.filter(id_resort='Elbrus').aggregate(Count('complexity'))
# m = SkyTrail.objects.filter(id_resort='Elbrus').aggregate(Max('height_difference'))
# max_height = SkiResort.skytrail_set.all().(max('height_difference'))


#  Blog.objects.values("entry__authors").annotate(entries=Count("entry"))
#  all_trail = self.skytrail_set.all().values_list('complexity').annotate(total=Count('complexity'))
#  SkyTrail.objects.aggregate(total=Count('complexity'))
#  SkyTrail.objects.values('complexity').annotate(total=Count('complexity'))
#  SkyTrail.objects.filter(id_resort='Elbrus').values('complexity').annotate(total=Count('complexity'))
#  SkyTrail.objects.all().values('id_resort__name').annotate(Count('complexity'))
#  SkyTrail.objects.all().values('id_resort__name', 'complexity').annotate(Count('complexity'))

# qs = SkiResort.objects.values('name').annotate(Count('complexity'))
# # 	.skytrail_set.all().values('id_resort__name', 'complexity').annotate(Count('complexity'))

# .skytrail_set.all().filter(id_resort='id_resort.name').values('complexity').annotate(total=Count('complexity'))

# h = SkiResort.objects.all()

# m = SkiPass.objects.filter(unified=1).values('price')

# SkiResort.objects.filter(skytrail__complexity='green')
# SkiResort.objects.filter(skytrail__complexity='green').distinct('name')
# SkiResort.objects.distinct().filter(skytrail__complexity='green')
