# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-03 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0033_auto_20171228_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='source',
            field=models.CharField(default='DMS', max_length=20),
        ),
    ]
