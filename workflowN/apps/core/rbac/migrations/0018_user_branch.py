# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-02-22 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0006_branch'),
        ('rbac', '0017_user_configuration_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.Branch'),
        ),
    ]