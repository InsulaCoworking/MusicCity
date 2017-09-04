# coding=utf-8
import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToCover, ResizeToFit

from bands.models import Band, Venue


def poster_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = '%s%s' % (uuid.uuid4(), extension)
    return os.path.join('event', str(instance.event_uid), filename)


class Event(models.Model):
    bands = models.ManyToManyField(Band, verbose_name='Bandas')
    venue = models.ForeignKey(Venue, related_name='venue')
    day = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=60)
    title = models.TextField(null=True, blank=True, verbose_name='Título del evento')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    created_by = models.ForeignKey(User, null=True, blank=True, verbose_name='Creado por')
    event_uid = models.UUIDField(default=uuid.uuid4, editable=False)
    poster = ProcessedImageField(null=True, blank=True, upload_to=poster_path, processors=[ResizeToFit(900,900, upscale=False)], format='JPEG', verbose_name='Imagen del evento')
    price = models.FloatField(null=True, blank=True, verbose_name='Precio')
    ticketLink = models.TextField(null=True, blank=True, verbose_name='Enlace compra de entradas')

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.band.name + ' - ' + str(self.day)
