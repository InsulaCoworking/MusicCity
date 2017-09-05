# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-05 14:53
from __future__ import unicode_literals

import bands.helpers
from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0031_auto_20170904_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='P\xe1gina de Facebook'),
        ),
        migrations.AddField(
            model_name='venue',
            name='profile_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('venue/'), verbose_name='Imagen de perfil'),
        ),
        migrations.AddField(
            model_name='venue',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Perfil de Twitter'),
        ),
        migrations.AddField(
            model_name='venue',
            name='webpage_link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='P\xe1gina web'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('venue/'), verbose_name='Imagen de cabecera'),
        ),
    ]
