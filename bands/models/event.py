import os
import uuid

from django.contrib.auth.models import User
from django.db import models

from bands.models import Band, Venue

def poster_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return os.path.join('event', instance.event_uid, '%s%s' % (uuid.uuid4(), extension))

class Event(models.Model):
    band = models.ForeignKey(Band, related_name='events')
    venue = models.ForeignKey(Venue, related_name='venue')
    day = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=60)
    created_by = models.ForeignKey(User, null=True, verbose_name='Creado por')
    event_uid = models.UUIDField(default=uuid.uuid4, editable=False)
    poster = models.ImageField(null=True, blank=True, upload_to=poster_path, verbose_name='Imagen del evento')
    price = models.FloatField(null=True, blank=True, verbose_name='Precio')
    ticketLink = models.TextField(null=True, verbose_name='Enlace compra de entradas')

    class Meta:
        verbose_name = 'Concierto'
        verbose_name_plural = 'Conciertos'
        ordering = ['day', 'time']

    def __unicode__(self):
        return self.band.name + ' - ' + str(self.day)
