# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName
from bands.models import Tag


class Band(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tag = models.ForeignKey(Tag, related_name="band_tag")
    genre = models.CharField(null=True, blank=True, verbose_name='etiqueta', max_length=240)
    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('band/'),
                                 processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG', verbose_name='Imagen principal')
    band_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('band/'),
                                        processors=[ResizeToFit(1200, 600, upscale=False)], format='JPEG',
                                        verbose_name='Imagen de cabecera')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                      processors=[ResizeToFill(150, 150, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 70})

    city = models.CharField(null=True, blank=True, verbose_name='Ciudad', max_length=140)
    num_members = models.IntegerField(null=True, blank=True, default=1)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    embed_code = models.TextField(null=True, blank=True, verbose_name='Códido embed para escucha (Bandcamp, Soundcloud, Spotify...')
    embed_media = models.TextField(null=True, blank=True, verbose_name='Códido embed de vídeo (Youtube, Vimeo...')

    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    youtube_link = models.CharField(null=True, blank=True, verbose_name='Canal de Youtube', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    bandcamp_link = models.CharField(null=True, blank=True, verbose_name='Página de BandCamp', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    presskit_link = models.CharField(null=True, blank=True, verbose_name='Presskit', max_length=250)
    spotify_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Spotify', max_length=250)

    owner = models.ForeignKey(User, null=True, blank=True, verbose_name="Responsable")

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'
        ordering = ['name']
        permissions = (
            ("manage_band", "Puede gestionar bandas"),
        )

    def __unicode__(self):
        return self.name


class BandToken(models.Model):
    token = models.CharField(null=False, verbose_name='Nombre', max_length=40, unique=True)
    band = models.ForeignKey(Band)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ':' + self.token
