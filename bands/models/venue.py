# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from bands.helpers import RandomFileName


class Venue(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, verbose_name='Responsable')
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    description = models.TextField(null=False, blank=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('venue/'),
                                 processors=[ResizeToFit(900, 900, upscale=False)], format='JPEG')
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Escenario'
        verbose_name_plural = 'Escenarios'
        ordering = ['name']

    def __unicode__(self):
        return self.name