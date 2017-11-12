# coding=utf-8
import datetime
from django.contrib.syndication.views import Feed
from django.urls import reverse

from bands.models import Event



class NextEventsFeed(Feed):
    title = "Alcalá es Música: próximos conciertos"
    link = '/events/'
    description = "Consulta los próximos conciertos de grupos alcalaínos o en espacios de Alcalá, recopilados por Alcalá es Música"
    title_template = "event/feed.html"

    def items(self):
        today = datetime.date.today()
        return Event.objects.filter(day__gte=today).order_by('day')[:9]

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('event_detail', kwargs={'pk':item.pk})