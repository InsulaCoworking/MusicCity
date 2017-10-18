# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone

from bands.forms.band import BandForm
from bands.helpers import get_query
from bands.models import Event, Tag, Band, BandToken


def bands_list(request):

    bands = Band.objects.all()
    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        bands = bands.filter(tag__pk=tag_filter)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name', 'genre', 'city'])
        if entry_query:
            bands = bands.filter(entry_query)

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

    params = {
            'ajax_url': reverse('bands_list'),
            'query_string':query_string,
            'bands': bands,
            'page': page
    }

    if request.is_ajax():
        response = render(request, 'band/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['tags'] = Tag.objects.filter(band_tag__isnull=False).distinct()
        return render(request, 'band/list.html', params)


def band_detail(request, pk):
    band = get_object_or_404(Band, pk=pk)
    today = datetime.date.today()
    events = Event.objects.filter(bands__id=band.id, day__gte=today)

    can_edit = request.user.is_authenticated() and (request.user.is_superuser or (
                    request.user == band.owner ))

    return render(request, 'band/detail.html', {
        'band': band,
        'events': events,
        'can_edit': can_edit,
        'view': request.GET.get('view', None)
    })


@login_required
def band_edit(request, pk):

    band = get_object_or_404(Band, pk=pk)

    can_edit = False
    if request.user.is_superuser or (
                request.user.has_perm('bands.manage_band') and request.user == band.owner):
        can_edit = True

    if not can_edit:
        return redirect(reverse('band_detail', kwargs={'pk':band.pk} ) + '?permissions=false')

    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, instance=band)
        if form.is_valid():
            band = form.save()
            return redirect('band_detail', pk=band.pk)
        else:
            print form.errors.as_data()
    else:
        form = BandForm(instance=band)
    return render(request, 'band/edit.html', { 'form': form, 'band':band })


def edit_band_token(request, token):
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
    return render(request, 'band/edit_token.html', {'band':band, 'form': form, 'save_success': save_success })
