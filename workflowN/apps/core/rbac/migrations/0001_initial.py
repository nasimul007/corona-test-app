# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-14 13:35
from __future__ import unicode_literals

import apps.core.rbac.manager
import apps.core.rbac.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50', regex='[-a-zA-Z0-9_.]{4,50}$')], verbose_name='user name')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=apps.core.rbac.models.avatar_dir)),
                ('address', models.CharField(blank=True, max_length=120)),
                ('phone_number', models.CharField(blank=True, max_length=14)),
                ('position', models.CharField(max_length=50)),
                ('expiry_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('status', models.CharField(choices=[('0', 'Inactive'), ('1', 'Active'), ('2', 'Vacation'), ('3', 'Expired')], max_length=50)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', apps.core.rbac.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='Group contains alphanumeric, underscore, space and period(.). Length: 2 to 100', regex='[-a-zA-Z0-9_.\\s]{2,100}$')])),
                ('status', models.BooleanField(default=True)),
                ('user', models.ManyToManyField(blank=True, related_name='group', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('active', models.BooleanField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('permission', models.ManyToManyField(related_name='permissions', to='rbac.Permission')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user', to='rbac.Role'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]