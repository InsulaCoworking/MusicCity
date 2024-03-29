# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Count, Case, When, CharField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bands.forms.venue import VenueForm
from bands.models import Venue, Event


def venues_list(request):

    venues = list(Venue.objects.all())
    random.shuffle(venues)
    venues.sort(key=lambda v: 1 if v.public_space else 0)
    return render(request, 'venue/list.html', {'venues': venues})


def venues_map_info(request):

    today = datetime.date.today()
    venues = Venue.objects.all()
    values = ['id', 'name', 'latitude', 'longitude', 'address', 'profile_image']


    if ('type' in request.GET) and request.GET['type'].strip():
        type = request.GET['type']
        if (type == 'recent_events'):
            venues = venues.annotate(eventscount=Case(
                        When(venue__day__gte=today, then=1),
                        output_field=CharField(),
                    ))\
                .filter(eventscount__gt=0)
            values += 'eventscount'

    venues = venues.values()
    data = list(venues)
    return JsonResponse(data, safe=False, content_type="application/json")


def venue_detail(request, pk):

    today = datetime.date.today()
    venue = get_object_or_404(Venue, pk=pk)
    events = Event.objects.filter(venue=venue, day__gte=today)

    can_edit = False
    if request.user.is_authenticated:
        if request.user.is_superuser or (
                    request.user.has_perm('bands.manage_venue') and request.user == venue.owner ):
            can_edit = True

    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': events,
        'can_edit': can_edit
    })


@login_required
def venue_edit(request, pk):

    venue = get_object_or_404(Venue, pk=pk)

    can_edit = False
    if request.user.is_superuser or (
                request.user.has_perm('bands.manage_venue') and request.user == venue.owner):
        can_edit = True

    if not can_edit:
        return redirect(reverse('venue_detail', kwargs={'pk':venue.pk} ) + '?permissions=false')

    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            venue = form.save()
            return redirect('venue_detail', pk=venue.pk)

    else:
        form = VenueForm(instance=venue)
    return render(request, 'venue/edit.html', { 'form': form, 'venue':venue })


@login_required
def venue_add(request):

    can_edit = False
    if request.user.is_superuser or request.user.has_perm('bands.manage_venue'):
        can_edit = True

    if not can_edit:
        return redirect( reverse('dashboard') + '?permissions=false' )

    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user
            venue.save()
            return redirect('venue_detail', pk=venue.pk)

    else:
        form = VenueForm()

    return render(request, 'venue/edit.html', { 'is_new': True, 'form': form, 'venue': None })


def venue_history(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    events = Event.objects.filter(venue=venue).order_by('-day')

    eventsbyyear = []
    for event in events:
        year = None

        for eventsyear in eventsbyyear:
            if event.day != None and eventsyear['year'] == event.day.year:
                year = eventsyear
                break

        if year is None:
            year = {'year': event.day.year, 'events': []}
            eventsbyyear.append(year)
        year['events'].append(event)

    return render(request, 'venue/history.html', {
        'venue': venue,
        'eventsbyyear': eventsbyyear
    })

'''
def venue_detail(request, pk):

    venue = get_object_or_404(Venue, pk=pk)
    events = Event.objects.filter(venue=venue)

    eventsbyday = []
    for event in events:
        day = None

        for eventsday in eventsbyday:
            if eventsday['day'] == event.day:
                day = eventsday
                break

        if day is None:
            day = {'day': event.day, 'events': []}
            eventsbyday.append(day)
        day['events'].append(event)

    for day in eventsbyday:
        day['events'].sort(helpers.order_latenight)

    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': eventsbyday,
    })
'''