# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 23:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('openref', '0003_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='Provider',
        ),
        migrations.RemoveField(
            model_name='review',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='review',
            name='product',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.AddField(
            model_name='providerupdate',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='openref.Provider'),
        ),
    ]