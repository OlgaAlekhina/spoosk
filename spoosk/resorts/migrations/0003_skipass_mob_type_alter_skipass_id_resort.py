# Generated by Django 4.2.5 on 2023-10-27 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0002_skireview_skiresort_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='skipass',
            name='mob_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='skipass',
            name='id_resort',
            field=models.ForeignKey(db_column='ID_resort', on_delete=django.db.models.deletion.DO_NOTHING, related_name='resorts', to='resorts.skiresort'),
        ),
    ]
