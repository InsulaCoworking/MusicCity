# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from bands.forms.band import BandForm
from bands.models import Event, Tag, Band, BandToken


def bands_list(request):

    bands = Band.objects.all()
    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        bands = bands.filter(tag__pk=tag_filter)

    paginator = Paginator(bands, 6)
    page = request.GET.get('page')
    try:
        bands = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bands = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        bands = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'band/search_results.html', {
            'bands': bands, 'page': page
        })
    else:
        tags = Tag.objects.filter(band_tag__isnull=False).distinct()
        return render(request, 'band/list.html', {
            'bands': bands, 'tags': tags, 'page': page
        })

def band_detail(request, pk):
    band = get_object_or_404(Band, pk=pk)
    events = Event.objects.filter(bands__id=band.id)
    return render(request, 'band/detail.html', {
        'band': band,
        'events': events,
        'view': request.GET.get('view', None)
    })

def edit_band(request, token):
    token = BandToken.objects.filter(token=token)
    if not token or not token[0].band or (token[0].expiration_date and token[0].expiration_date >= timezone.now()):
        return render(request, 'band/badtoken.html', {'token': token})

    band = token[0].band
    save_success = False
    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, instance=band)
        print form.is_valid()
        if form.is_valid():
            band = form.save()
            print band.band_image
            save_success = True
    else:
        form = BandForm(instance=band)
    return render(request, 'band/edit.html', {'band':band, 'form': form, 'save_success': save_success })
