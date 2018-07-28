from django.shortcuts import get_object_or_404, render

from bands.models import Band
from microsite.models import Microsite


def microsite_index(request, slug):
    microsite = get_object_or_404(Microsite, slug=slug)

    bands = Band.objects.filter(events__id__in=microsite.events.all()).distinct()
    return render(request, 'microsite/index.html', {
        'microsite': microsite,
        'bands':bands,
    })