from unicodedata import category

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from bands.models import Band
from microsite.models import Microsite
from puput.models import BlogPage, EntryPage, Category

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
            context['entries'] = EntryPage.objects.filter(tags__slug__in=[self.object.news_tag]).distinct()

        return context


class MicrositeList(ListView):
    model = Microsite
    paginate_by = 6
    queryset = Microsite.objects.all().order_by('-start_date')
    template_name = 'microsite/list.html'
