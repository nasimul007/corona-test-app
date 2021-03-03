# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-10-09 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpmn', '0024_application_initiated_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailQueues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_e', models.EmailField(default='webmaster@localhost', max_length=254)),
                ('to', models.EmailField(max_length=254)),
                ('cc', models.TextField(blank=True, null=True)),
                ('subject', models.TextField()),
                ('body', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]