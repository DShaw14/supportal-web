# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-16 19:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0010_auto_20161116_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='createdBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
