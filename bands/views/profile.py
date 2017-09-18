import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bands.models import Venue, Band, Event


def can_manage_events(user):
    if user.has_perm('bands.manage_events'):
        return True
    else:
        if Venue.objects.filter(owner=user).count() > 0:
            return True
        elif Band.objects.filter(owner=user).count() > 0:
            return True
        else:
            return False


@login_required
def profile(request):

    params = {}
    if request.user.has_perm('bands.manage_venue'):
        params['manage_venue'] = True
        venues = Venue.objects.filter(owner=request.user)[:1]
        if len(venues) >= 1:
            params['venue'] = venues[0]
            params['manage_event'] = True
        else:
            params['prompt_new_venue'] = True

    bands = Band.objects.filter(owner=request.user)[:1]
    if can_manage_events(request.user):
        params['manage_event'] = True

    print params

    return render(request, 'profile/index.html', params)


@login_required
def user_events(request):

    params = {}
    if can_manage_events(request.user):
        params['manage_event'] = True

    today = datetime.date.today()
    params['events'] = Event.objects.filter(created_by=request.user, day__gte=today)

    return render(request, 'profile/events.html', params)


@login_required
def user_history(request):

    params = {}
    if can_manage_events(request.user):
        params['manage_event'] = True

    today = datetime.date.today()
    params['events'] = Event.objects.filter(created_by=request.user, day__lt=today)

    return render(request, 'profile/history.html', params)