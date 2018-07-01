# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecocases', '0018_masseffectpotential_masseffectpotentialeval'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReboundPotential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
                ('label', models.CharField(max_length=50)),
                ('color', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ReboundPotentialEval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecocase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocases.Ecocase')),
                ('reboundpotential', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecocases.ReboundPotential')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
