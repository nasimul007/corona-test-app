# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-08 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0014_auto_20171107_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdelegate',
            name='start_date',
            field=models.DateField(verbose_name='start_date'),
        ),
    ]
