# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-14 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0044_auto_20180206_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='tag',
        ),
        migrations.AddField(
            model_name='professional',
            name='tags',
            field=models.ManyToManyField(default=None, related_name='pros', to='bands.ProfessionalTag', verbose_name='Categor\xedas'),
        ),
    ]