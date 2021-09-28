# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from image_cropping import ImageRatioField
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName
from bands.models import Tag


class Band(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    tag = models.ForeignKey(Tag, null=True, related_name="band_tag", on_delete=models.SET_NULL)
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

    profile_thumb = ImageRatioField('profile_image', '200x200')

    city = models.CharField(null=True, blank=True, verbose_name='Ciudad', max_length=140)
    num_members = models.IntegerField(null=True, blank=True, default=1)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    embed_code = models.TextField(null=True, blank=True, verbose_name='Códido embed para escucha (Bandcamp, Soundcloud, Spotify...')
    embed_media = models.TextField(null=True, blank=True, verbose_name='Códido embed de vídeo (Youtube, Vimeo...')

    facebook_link  = models.CharField(null=True, blank=True, max_length=250, verbose_name='Página de Facebook')
    youtube_link   = models.CharField(null=True, blank=True, max_length=250, verbose_name='Canal de Youtube')
    twitter_link   = models.CharField(null=True, blank=True, max_length=250, verbose_name='Perfil de Twitter')
    instagram_link = models.CharField(null=True, blank=True, max_length=250, verbose_name='Perfil de Instagram')
    bandcamp_link  = models.CharField(null=True, blank=True, max_length=250, verbose_name='Página de BandCamp')
    webpage_link   = models.CharField(null=True, blank=True, max_length=250, verbose_name='Página web')
    presskit_link  = models.CharField(null=True, blank=True, max_length=250, verbose_name='Presskit')
    spotify_link   = models.CharField(null=True, blank=True, max_length=250, verbose_name='Perfil de Spotify')

    owner = models.ForeignKey(User, null=True, blank=True, verbose_name="Responsable", on_delete=models.SET_NULL)
    hidden_in_catalog = models.BooleanField(default=False, verbose_name="Oculto en el listado principal",
                                            help_text="Ocultar el perfil del listado, para bandas que no son de Alcala pero se crea su perfil para ciclos y festivales")

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'
        ordering = ['name']
        permissions = (
            ("manage_band", "Puede gestionar bandas"),
        )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class BandToken(models.Model):
    token = models.CharField(null=False, verbose_name='Nombre', max_length=40, unique=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ':' + self.token
