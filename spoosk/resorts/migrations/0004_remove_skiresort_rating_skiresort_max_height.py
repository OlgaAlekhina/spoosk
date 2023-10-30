# Generated by Django 4.2.5 on 2023-10-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0003_skipass_mob_type_alter_skipass_id_resort'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skiresort',
            name='rating',
        ),
        migrations.AddField(
            model_name='skiresort',
            name='max_height',
            field=models.IntegerField(blank=True, help_text='maximum height of resort', null=True),
        ),
    ]
