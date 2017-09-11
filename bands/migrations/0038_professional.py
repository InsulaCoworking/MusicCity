# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-11 12:10
from __future__ import unicode_literals

import bands.helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bands', '0037_auto_20170907_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Nombre')),
                ('description', models.TextField(blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('venue/'), verbose_name='Imagen de cabecera')),
                ('profile_image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=bands.helpers.RandomFileName('venue/'), verbose_name='Imagen de perfil')),
                ('embed_code', models.TextField(blank=True, null=True, verbose_name='C\xf3dido embed para escucha (Bandcamp, Soundcloud, Spotify...')),
                ('embed_media', models.TextField(blank=True, null=True, verbose_name='C\xf3dido embed de v\xeddeo (Youtube, Vimeo...')),
                ('facebook_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='P\xe1gina de Facebook')),
                ('twitter_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Perfil de Twitter')),
                ('webpage_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='P\xe1gina web')),
                ('youtube_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Canal de Youtube')),
                ('presskit_link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Presskit')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Profesional',
                'verbose_name_plural': 'Profesionales',
            },
        ),
    ]