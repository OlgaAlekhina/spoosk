from decimal import Decimal
from itertools import product

from django.db import models
from django.db.models import Sum, Max, Count
from django.urls import reverse


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
    id_resort = models.ForeignKey('SkiResort', models.DO_NOTHING, db_column='ID_resort')  # Field name made lowercase.
    type = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    adult = models.IntegerField(blank=True, null=True)
    childlike = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unified = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ski_pass'


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
    image = models.ImageField('image', upload_to="static/image/card", null=True, help_text="url of small image for resort's card")
    list_month = models.TextField(blank=True, null=True, help_text="list of months which cover the ski season")
    link_ofsite = models.CharField(blank=True, null=True, help_text="url of resort's website")
    main_resort_img = models.ImageField('image', upload_to="static/image/resorts", null=True, help_text="url of large image for resort's page header")

    class Meta:
        managed = True
        db_table = 'ski_resort'

    def __str__(self):
        return f'{self.name} {self.region} {self.list_month}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse("resort_detail", kwargs={"slug": self.name})

    @property
    def total_length_calculation(self):
        total = self.skytrail_set.all().aggregate(Sum('extent'))
        result = round(total['extent__sum']//1000)
        return result

    @property
    def max_height_difference(self):
        max_height = self.skytrail_set.all().aggregate(Max('height_difference'))
        result = max_height['height_difference__max']
        return result

    @property
    def ski_pass_one(self):
        price_skipass = self.skipass_set.all().filter(unified=1).values('price')
        price_skipass_list = list(price_skipass)
        if len(price_skipass_list):
            result = price_skipass_list
        else:
            result = [{'price': Decimal('0')}]

        return result[0]

    @property
    def skipass_min(self):
        skipass_price = self.skipass_set.order_by('price').first()
        skipass_min = skipass_price.price

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
        all_trail = self.skilifts_set.all().aggregate(armchair=Sum('armchair'), bugelny=Sum('bugelny'), gondola=Sum('gondola'), travelators=Sum('travelators'))

        return all_trail

    @property
    def trail_number_count(self):
        trail_number = len(self.skytrail_set.all())
        return trail_number

    @property
    def type_name_price(self):
        all_trail = self.skipass_set.all().values('type', 'name', 'price')
        return all_trail


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


class Month(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'month'

    def __str__(self):
        return {self.name}

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


class Review(models.Model):
    author = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ваше имя')
    riding_level = models.ForeignKey(RidingLevel, models.DO_NOTHING, verbose_name='Ваш уровень катания', blank=True, null=True, )
    resort = models.ForeignKey(SkiResort,  models.DO_NOTHING, db_column='ID_resort')
    text_review = models.TextField(blank=True, null=True, verbose_name='Ваш отзыв')
    # image_review = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'review'

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
