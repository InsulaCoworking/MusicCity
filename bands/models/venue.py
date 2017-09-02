# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from bands.helpers import RandomFileName


class Venue(models.Model):
    owner = models.ForeignKey(User, null=True, verbose_name='Responsable')
    name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    description = models.TextField(null=False, blank=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    image = models.ImageField(null=True, blank=True, upload_to=RandomFileName('venue/'))
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Escenario'
        verbose_name_plural = 'Escenarios'
        ordering = ['name']

    def __unicode__(self):
        return self.name