# Generated by Django 4.2.5 on 2023-12-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0009_skiresort_link_map_alter_resortimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resortimage',
            name='image',
            field=models.ImageField(upload_to='resorts/extra'),
        ),
        migrations.AlterField(
            model_name='skiresort',
            name='image',
            field=models.ImageField(help_text="url of small image for resort's card", null=True, upload_to='resorts/mini'),
        ),
        migrations.AlterField(
            model_name='skiresort',
            name='main_resort_img',
            field=models.ImageField(help_text="url of large image for resort's page header", null=True, upload_to='resorts/maxi'),
        ),
    ]