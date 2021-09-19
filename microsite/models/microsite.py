# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName
from bands.models import Tag, Event


class Microsite(models.Model):
    title = models.CharField(null=False, verbose_name='Título', max_length=240)
    slug = models.SlugField(null=False, verbose_name='Slug (url)', unique=True, max_length=100)
    day = models.DateField(null=True, blank=True, auto_now_add=True)
    news_tag = models.CharField(null=True, blank=True, max_length=100, verbose_name='Tag de noticias')

    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('special/'),
                                 processors=[ResizeToFit(1200, 512, upscale=False)], format='PNG', verbose_name='Imagen principal')
    top_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('special/'),
                                        processors=[ResizeToFit(1200, 600, upscale=False)], format='JPEG',
                                        verbose_name='Imagen fondo de cabecera')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                      processors=[ResizeToFill(150, 150, upscale=False)],
                                      format='JPEG',
                                      options={'quality': 70})

    start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin')

    primary_bg  = models.CharField(null=False, verbose_name='Color de fondo principal', max_length=10)
    primary_text = models.CharField(null=False, verbose_name='Color de texto principal', max_length=10)
    secondary_bg = models.CharField(null=False, verbose_name='Color de fondo secundario', max_length=10)
    secondary_text = models.CharField(null=False, verbose_name='Color de texto secundario', max_length=10)

    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    embed_code = models.TextField(null=True, blank=True, verbose_name='Códido embed 1')
    embed_media = models.TextField(null=True, blank=True, verbose_name='Códido embed 2')

    events = models.ManyToManyField(Event, blank=True, verbose_name="Eventos", related_name="microsites")

    class Meta:
        verbose_name = 'Microsite especial'
        verbose_name_plural = 'Microsites especiales'
        ordering = ['day']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

