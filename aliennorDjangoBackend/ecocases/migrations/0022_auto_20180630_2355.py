# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 23:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecocases', '0021_ecocasegeneraleval'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ecocasegeneraleval',
            old_name='case_characterizations_comments',
            new_name='case_characterizations_comment',
        ),
    ]