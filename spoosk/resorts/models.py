from django.db import models


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
    adult = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    childlike = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    unified = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ski_pass'


class SkiResort(models.Model):
    id_resort = models.CharField(db_column='ID_resort', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    begin_season = models.CharField(max_length=50, blank=True, null=True)
    end_season = models.CharField(max_length=50, blank=True, null=True)
    freeride = models.IntegerField(blank=True, null=True)
    snowpark = models.IntegerField(blank=True, null=True)
    evening_skiing = models.IntegerField(blank=True, null=True)
    school = models.IntegerField(blank=True, null=True)
    ind_training = models.IntegerField(blank=True, null=True)
    children_school = models.IntegerField(blank=True, null=True)
    equip_rental = models.IntegerField(blank=True, null=True)
    distance_airport = models.IntegerField(blank=True, null=True)
    distance_railway = models.IntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ski_resort'


class SkyTrail(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=20)  # Field name made lowercase.
    id_resort = models.ForeignKey(SkiResort, models.DO_NOTHING, db_column='ID_resort')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=True, null=True)
    complexity = models.CharField(max_length=5, blank=True, null=True)
    extent = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    height_difference = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sky_trail'
