# coding=utf-8
import datetime
from django.contrib.syndication.views import Feed
from django.urls import reverse

from bands.models import Event
from bands.rss.event_feed import ExtendedEventRSSFeed


class NextEventsFeed(Feed):
    feed_type = ExtendedEventRSSFeed
    title = "Alcalá es Música: próximos conciertos"
    link = '/events/'
    description = "Consulta los próximos conciertos de grupos alcalaínos o en espacios de Alcalá, recopilados por Alcalá es Música"
    title_template = "event/feed.html"

    def item_extra_kwargs(self, item):
        extra = super(NextEventsFeed, self).item_extra_kwargs(item)
        extra.update({'ev_startdate': self.item_startdate(item)})
        extra.update({'ev_location': self.item_location(item)})
        extra.update({'dc_subject': self.item_subject(item)})
        return extra

    def items(self):
        today = datetime.date.today()
        return Event.objects.filter(day__gte=today).order_by('day')[:9]

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('event_detail', kwargs={'pk':item.pk})

    def item_startdate(self, item):
        return item.day.strftime("%d/%m/%Y")

    def item_location(self, item):
        return item.venue_title

    def item_subject(self, item):
        return str(item)