from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from bands.models import Band
from microsite.models import Microsite
from zinnia.models.entry import Entry

class MicrositeIndex(DetailView):
    model = Microsite
    context_object_name = 'microsite'
    template_name = 'microsite/index.html'

    def get_object(self, queryset=None):
        return Microsite.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bands'] = Band.objects.filter(events__id__in=self.object.events.all()).distinct()
        if self.object.news_tag:
            context['entries'] = Entry.published.filter(tags__icontains=self.object.news_tag)

        return context


class MicrositeList(ListView):
    model = Microsite
    queryset = Microsite.objects.all().order_by('-start_date')
    template_name = 'microsite/list.html'
