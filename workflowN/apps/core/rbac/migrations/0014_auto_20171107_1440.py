# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-07 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0013_userdelegate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdelegate',
            name='end_date',
            field=models.DateField(verbose_name='end_date'),
        ),
        migrations.AlterField(
            model_name='userdelegate',
            name='start_date',
            field=models.DateField(auto_now_add=True, verbose_name='start_date'),
        ),
    ]