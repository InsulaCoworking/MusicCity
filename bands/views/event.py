import datetime
from django.shortcuts import render, get_object_or_404

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

    events = Event.objects.all()

    today = datetime.date.today()
    thisweek_start = today - datetime.timedelta(days=today.weekday())
    thisweek_end = today + datetime.timedelta(days=6)
    nextweek_start = thisweek_start + datetime.timedelta(weeks=1)
    nextweek_end = thisweek_end + datetime.timedelta(weeks=1)

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('start_date', None)

    if start_date is None and end_date is None:
        start_date = thisweek_start
        end_date = thisweek_end


    venue_filter = request.GET.get('venue', None)
    tag_filter = request.GET.get('tag', None)
    day_filter = request.GET.get('day', None)


    if venue_filter:
        events = events.filter(venue__pk=venue_filter)
    if tag_filter:
        events = events.filter(band__tag__pk=tag_filter)

    if request.is_ajax():
        pass
    else:
        tags = Tag.objects.all()
        venues = Venue.objects.all()

        return render(request, 'event/schedule.html', {
            'events': events,
            'tags': tags,
            'venues': venues,
            'venue_filter': venue_filter,
            'dates': {
                'thisweek_start': thisweek_start,
                'thisweek_end':thisweek_end,
                'nextweek_start': nextweek_start,
                'nextweek_end': nextweek_end
            }
        })