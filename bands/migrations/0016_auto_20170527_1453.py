# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0015_auto_20170525_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='band_tag', to='bands.Tag'),
        ),
    ]
