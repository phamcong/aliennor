# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-17 21:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecocases', '0002_auto_20180317_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecocase',
            name='evaluated_by_users',
        ),
        migrations.AddField(
            model_name='ecocase',
            name='evaluated_by_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
