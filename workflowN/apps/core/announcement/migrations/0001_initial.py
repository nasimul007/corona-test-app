# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-14 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'User'), ('2', 'Group'), ('3', 'All Users')], max_length=50)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
            ],
        ),
    ]
