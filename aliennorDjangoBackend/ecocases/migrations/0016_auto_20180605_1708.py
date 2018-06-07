# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecocases', '0015_auto_20180522_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecocase',
            name='evaluate_by_users',
            field=models.ManyToManyField(related_name='evaluate_by_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='evaluated_by_users',
            field=models.ManyToManyField(related_name='evaluated_by_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
