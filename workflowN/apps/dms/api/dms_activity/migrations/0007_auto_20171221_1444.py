# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-21 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms_activity', '0006_auto_20171221_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmsactivity',
            name='activity_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]