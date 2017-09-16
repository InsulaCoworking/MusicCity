import datetime

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.shortcuts import render, get_object_or_404

from bands.helpers import get_query
from bands.models import Event, Tag, Venue


def event_detail(request, pk):

    event = get_object_or_404(Event, pk=pk)

    can_edit = False
    if request.user.is_authenticated():
        if request.user.is_superuser or request.user == event.created_by:
            can_edit = True

    return render(request, 'event/detail.html', {
        'event': event,
        'can_edit': can_edit
    })


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

    paginator = Paginator(events, 3)
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