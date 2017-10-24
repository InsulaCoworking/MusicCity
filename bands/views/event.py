import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bands.forms.event import EventForm
from bands.helpers import get_query
from bands.models import Event, Tag, Venue, Band


def can_edit_event(user, event):
    return user.is_authenticated() and (
                user.is_superuser
            or (
                user == event.created_by and event.day > datetime.date.today()
            ))

def events_schedule(request):

    today = datetime.date.today()
    thisweek_start = today - datetime.timedelta(days=today.weekday())
    thisweek_end = thisweek_start + datetime.timedelta(days=6)
    nextweek_start = thisweek_start + datetime.timedelta(weeks=1)
    nextweek_end = thisweek_end + datetime.timedelta(weeks=1)

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    date_filter = False
    if start_date is not None and end_date is not None:
        date_filter = True
        start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    else:
        start_date = thisweek_start
        end_date = thisweek_end

    venue_filter = request.GET.get('venue', None)
    tag_filter = request.GET.get('tag', None)
    events = Event.objects.filter(day__lte=end_date, day__gte=start_date, venue__isnull=False)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'venue_name', 'venue__name', 'bands__name'])
        if entry_query:
            events = events.filter(entry_query)

    if venue_filter:
        events = events.filter(venue__pk=venue_filter)
    if tag_filter:
        events = events.filter(band__tag__pk=tag_filter)

    paginator = Paginator(events, 6)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    if request.is_ajax():
        response = render(request, 'event/search_results.html', {
            'events':events
        })
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        tags = Tag.objects.all()
        venues = Venue.objects.all()

        return render(request, 'event/schedule.html', {
            'events': events,
            'tags': tags,
            'venues': venues,
            'venue_filter': venue_filter,
            'date_filter': date_filter,
            'query_string': query_string,
            'dates': {
                'start_date': start_date,
                'end_date': end_date,
                'thisweek_start': thisweek_start,
                'thisweek_end':thisweek_end,
                'nextweek_start': nextweek_start,
                'nextweek_end': nextweek_end
            }
        })


def event_detail(request, pk):

    event = get_object_or_404(Event, pk=pk)
    can_edit = can_edit_event(request.user, event)

    return render(request, 'event/detail.html', {
        'event': event,
        'can_edit': can_edit
    })


@login_required
def event_add(request):

    params = { 'new_event': True }

    if ('band' in request.GET) and request.GET['band'].strip():
        band_pk = request.GET['band']
        band = Band.objects.get(pk=band_pk)
        if request.user.is_superuser or request.user == band.owner:
            params['preselect_band'] = band

    if request.user.has_perm('bands.manage_venue') and not request.user.has_perm('bands.manage_events'):
        # if user owns a venue, can create events in that venue
        params['manage_venue'] = True
        venues = Venue.objects.filter(owner=request.user)[:1]
        if len(venues) >= 1:
            params['venue'] = venues[0]
        else:
            params['prompt_new_venue'] = True

    if request.user.has_perm('bands.manage_band'):
        bands = Band.objects.filter(owner=request.user)
        if bands.count() == 1:
            params['preselect_band'] = bands[0]
        elif bands.count() > 1:
            params['choose_band'] = bands

    if request.user.has_perm('bands.manage_events') or 'preselect_band' in params:
        # can create events in any venue or with any band
        params['venues'] = Venue.objects.all()
        

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():

            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            event_bands = form.cleaned_data.get('event_bands')
            bands = event_bands.split(',')
            for order, band_pk in enumerate(bands):
                try:
                    pk = int(band_pk)
                    band = Band.objects.get(pk=pk)
                    event.bands.add(band)
                except:
                    pass

            event.save()

            return redirect('event_detail', pk=event.pk)
        else:
            print form.errors.as_data()
    else:
        if 'venue' in params:
            form = EventForm(initial={'venue':params['venue'].pk})
        else:
            form = EventForm()

    params['form'] = form

    return render(request, 'event/form.html', params)



@login_required
def event_edit(request, pk):

    event = get_object_or_404(Event, pk=pk)
    can_edit = can_edit_event(request.user, event)

    if not can_edit:
        return redirect(reverse('event_detail', kwargs={'pk': event.pk}) + '?permissions=false')

    params = { 'event': event }
    if request.user.has_perm('bands.manage_events'):
        # can create events in any venue or with any band
        params['venues'] = Venue.objects.all()
        params['venue'] = event.venue
    else:
        if request.user.has_perm('bands.manage_venue'):
            # if user owns a venue, can create events in that venue
            params['manage_venue'] = True
            params['venue'] = event.venue

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():

            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            event.bands.clear()
            event_bands = form.cleaned_data.get('event_bands')
            bands = event_bands.split(',')
            for order, band_pk in enumerate(bands):
                try:
                    pk = int(band_pk)
                    band = Band.objects.get(pk=pk)
                    event.bands.add(band)
                except:
                    pass
            event.save()

            return redirect('event_detail', pk=event.pk)
        else:
            print form.errors.as_data()
    else:
        form = EventForm(instance=event)

    params['form'] = form
    print params

    return render(request, 'event/form.html', params)
