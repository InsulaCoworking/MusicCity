# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName
from bands.models import ProfessionalTag


class Professional(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='Responsable', on_delete=models.CASCADE)
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tags = models.ManyToManyField(ProfessionalTag, default=None, verbose_name='Categorías', related_name="pros")
    description = models.TextField(null=False, blank=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('venue/'), verbose_name='Imagen de cabecera',
                                 processors=[ResizeToFit(900, 900, upscale=False)], format='JPEG')
    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('venue/'),
                                verbose_name='Imagen de perfil',
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    embed_code = models.TextField(null=True, blank=True,
                                  verbose_name='Códido embed para escucha (Bandcamp, Soundcloud, Spotify...')
    embed_media = models.TextField(null=True, blank=True, verbose_name='Códido embed de vídeo (Youtube, Vimeo...')

    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    youtube_link = models.CharField(null=True, blank=True, verbose_name='Canal de Youtube', max_length=250)
    presskit_link = models.CharField(null=True, blank=True, verbose_name='Presskit', max_length=250)

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['name']
        permissions = (
            ("manage_pro", "Puede gestionar un perfil profesional"),
        )

    def __unicode__(self):
        return self.name
