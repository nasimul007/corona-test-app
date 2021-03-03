# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-14 09:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0019_metadocumentjson_doc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_by', to=settings.AUTH_USER_MODEL),
        ),
    ]