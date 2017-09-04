# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-04 12:32
from __future__ import unicode_literals

import bands.helpers
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0029_auto_20170904_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='band_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('band/'), verbose_name='Imagen de cabecera'),
        ),
        migrations.AlterField(
            model_name='band',
            name='profile_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('band/'), verbose_name='Imagen principal'),
        ),
    ]
