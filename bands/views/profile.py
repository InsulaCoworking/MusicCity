from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bands.models import Venue, Band

@login_required
def profile(request):

    venue = None
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
    if len(bands) >= 1:
        params['manage_event'] = True

    print params

    return render(request, 'profile/index.html', params)
