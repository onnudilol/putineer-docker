# Generated by Django 2.0.6 on 2018-06-16 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20180616_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image_url',
            field=models.URLField(max_length=300),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='yelp_url',
            field=models.URLField(max_length=300),
        ),
    ]
