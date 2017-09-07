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

    if request.is_ajax():
        pass
    else:
        tags = Tag.objects.all()
        venues = Venue.objects.all()

        return render(request, 'event/schedule.html', {
            'events': events,
            'tags': tags,
            'venues': venues
        })