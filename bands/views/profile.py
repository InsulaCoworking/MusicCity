# coding=utf-8
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect

from bands.forms.profile import ProfileForm
from bands.forms.signup import SignUpForm
from bands.models import Venue, Band, Event, BandToken, Professional


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


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            user_type = form.cleaned_data.get('user_type')
            if user_type == 'venue':
                permission = Permission.objects.get(codename='manage_venue',)
                user.user_permissions.add(permission)
            elif user_type == 'band':
                permission = Permission.objects.get( codename='manage_band',)
                user.user_permissions.add(permission)
            elif user_type == 'pro':
                permission = Permission.objects.get(codename='manage_pro', )
                user.user_permissions.add(permission)

            login(request, user)

            token = form.cleaned_data.get('token')
            if token:
                bandtoken = BandToken.objects.filter(token=token)
                if bandtoken and bandtoken[0].band:
                    return redirect('link_band', token=token)

            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def profile(request):

    params = {}
    if request.user.has_perm('bands.manage_venue'):
        params['manage_venue'] = True
        venues = Venue.objects.filter(owner=request.user)[:1]
        if len(venues) >= 1:
            params['venue'] = venues[0]
        else:
            params['prompt_new_venue'] = True

    if request.user.has_perm('bands.manage_band'):
        params['manage_band'] = True
        params['bands'] = Band.objects.filter(owner=request.user)

    if request.user.has_perm('bands.manage_pro'):
        params['manage_pro'] = True
        params['pros'] = Professional.objects.filter(user=request.user)

    if can_manage_events(request.user):
        params['manage_event'] = True

    return render(request, 'profile/index.html', params)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()

    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/edit.html', {'profile_form': profile_form, 'password_form':password_form })

@login_required
def profile_save_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('edit_profile')
    else:
        password_form = PasswordChangeForm(user=request.user)

    profile_form = ProfileForm(instance=request.user)

    return render(request, 'profile/edit.html', {'profile_form': profile_form, 'password_form':password_form })

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