# Generated by Django 2.0.6 on 2018-06-20 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20180616_0020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='coordinates',
            new_name='coords',
        ),
    ]
