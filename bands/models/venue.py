# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName


class Venue(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, verbose_name='Responsable', on_delete=models.SET_NULL)
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    description = models.TextField(null=False, blank=True)
    latitude = models.FloatField(null=False, verbose_name='Latitud')
    longitude = models.FloatField(null=False, verbose_name='Longitud')
    image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('venue/'), verbose_name='Imagen de cabecera',
                                 processors=[ResizeToFit(900, 900, upscale=False)], format='JPEG')
    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('venue/'),
                                verbose_name='Imagen de perfil',
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})
    address = models.TextField(null=True, blank=True)
    public_space = models.BooleanField(default=False, verbose_name='Espacio en la vía pública')

    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)

    class Meta:
        verbose_name = 'Escenario'
        verbose_name_plural = 'Escenarios'
        ordering = ['name']
        permissions = (
            ("manage_venue", "Puede gestionar un espacio"),
        )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name