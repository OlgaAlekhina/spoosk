from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'month',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RidingLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'riding_level',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SkiResort',
            fields=[
                ('id_resort', models.CharField(db_column='ID_resort', max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('begin_season', models.CharField(blank=True, max_length=50, null=True)),
                ('end_season', models.CharField(blank=True, max_length=50, null=True)),
                ('freeride', models.IntegerField(blank=True, null=True)),
                ('snowpark', models.IntegerField(blank=True, null=True)),
                ('evening_skiing', models.IntegerField(blank=True, null=True)),
                ('school', models.IntegerField(blank=True, null=True)),
                ('ind_training', models.IntegerField(blank=True, null=True)),
                ('children_school', models.IntegerField(blank=True, null=True)),
                ('equip_rental', models.IntegerField(blank=True, null=True)),
                ('distance_airport', models.IntegerField(blank=True, null=True)),
                ('distance_railway', models.IntegerField(blank=True, null=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(null=True, upload_to='static/image/card', verbose_name='image')),
                ('list_month', models.TextField(blank=True, null=True)),
                ('link_ofsite', models.CharField(blank=True, null=True)),
                ('main_resort_img', models.ImageField(null=True, upload_to='static/image/resorts', verbose_name='image')),
            ],
            options={
                'db_table': 'ski_resort',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SkyTrail',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('complexity', models.CharField(blank=True, max_length=5, null=True)),
                ('extent', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('height_difference', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('id_resort', models.ForeignKey(db_column='ID_resort', on_delete=django.db.models.deletion.DO_NOTHING, to='resorts.skiresort')),
            ],
            options={
                'db_table': 'sky_trail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SkiPass',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=20, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('adult', models.IntegerField(blank=True, null=True)),
                ('childlike', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unified', models.IntegerField(blank=True, null=True)),
                ('id_resort', models.ForeignKey(db_column='ID_resort', on_delete=django.db.models.deletion.DO_NOTHING, to='resorts.skiresort')),
            ],
            options={
                'db_table': 'ski_pass',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SkiLifts',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('extent', models.IntegerField(blank=True, null=True)),
                ('armchair', models.IntegerField(blank=True, null=True)),
                ('bugelny', models.IntegerField(blank=True, null=True)),
                ('gondola', models.IntegerField(blank=True, null=True)),
                ('travelators', models.IntegerField(blank=True, null=True)),
                ('id_resort', models.ForeignKey(db_column='ID_resort', on_delete=django.db.models.deletion.DO_NOTHING, to='resorts.skiresort')),
            ],
            options={
                'db_table': 'ski_lifts',
                'managed': True,
            },
        ),
    ]
