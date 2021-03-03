# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-12 07:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0018_savesearch_search_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='savesearch',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
