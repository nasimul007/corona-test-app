# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-13 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpmn', '0011_appquery_query_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='appquery',
            name='answer_date',
            field=models.DateField(blank=True, null=True, verbose_name='answer_date'),
        ),
    ]