# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-13 13:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_restaurant_location'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Restaurant',
            new_name='RestaurantLocation',
        ),
    ]
