# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstApp', '0013_auto_20161212_1239'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnCallRotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oncall_clockin', models.TimeField(default=None, unique_for_date=True)),
                ('oncall_clockout', models.TimeField(default=None, unique_for_date=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='developer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
    ]
