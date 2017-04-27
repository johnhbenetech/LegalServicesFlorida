# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 22:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openref', '0009_auto_20170420_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='provider_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='providerupdate',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]