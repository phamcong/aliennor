# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-24 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecocases', '0010_auto_20180424_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecoeffectpotential',
            name='selected',
        ),
        migrations.RemoveField(
            model_name='ecoeffectpotentialeval',
            name='eco_effect_potentials',
        ),
        migrations.AddField(
            model_name='ecoeffectpotentialeval',
            name='eco_effect_potential',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecocases.EcoEffectPotential'),
        ),
        migrations.AddField(
            model_name='ecoeffectpotentialeval',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
