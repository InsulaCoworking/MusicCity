# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, UpdateView, CreateView, ListView

from bands.forms.band import BandForm, BandProfileImageForm
from bands.helpers import get_query
from bands.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from bands.models import Event, Tag, Band, BandToken


class BandList(ListView, AjaxTemplateResponseMixin):
    model = Band
    paginate_by = settings.BANDS_PER_PAGE
    queryset = Band.objects.filter(hidden_in_catalog=False)
    template_name = 'band/list.html'
    ajax_template_name = 'band/search_results.html'

    def get_queryset(self):
        bands = super().get_queryset()
        tag_filter = self.request.GET.get('tag', None)

        if tag_filter:
            bands = bands.filter(tag__pk=tag_filter)

        query_string = self.request.GET.get('q', None)
        if query_string:
            entry_query = get_query(query_string, ['name', 'genre', 'city'])
            if entry_query:
                bands = bands.filter(entry_query)

        return bands

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(band_tag__isnull=False).distinct()
        return context


class BandDetail(DetailView):
    model = Band
    context_object_name = 'band'
    template_name = 'band/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(bands__id=self.object.id, day__gte=datetime.date.today())
        context['can_edit'] = self.request.user.is_superuser or self.request.user == self.object.owner
        context['view'] = self.request.GET.get('view', None)
        return context


class BandEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'bands.manage_band'
    model = Band
    context_object_name = 'band'
    template_name = 'band/edit.html'
    form_class = BandForm

    def dispatch(self, request, *args, **kwargs):
        band = get_object_or_404(Band, pk=kwargs[self.pk_url_kwarg])
        if not (request.user.is_superuser or request.user == band.owner):
            return redirect(reverse('band_detail', kwargs={'pk': band.pk}) + '?permissions=false')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = BandProfileImageForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('band_detail', kwargs={'pk':self.object.pk})


class BandImageEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'bands.manage_band'
    model = Band
    context_object_name = 'band'
    template_name = 'band/edit.html'
    form_class = BandProfileImageForm

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('band_detail', kwargs={'pk':self.object.pk})


class AddBand(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'bands.manage_band'
    model = Band
    context_object_name = 'band'
    template_name = 'band/edit.html'
    form_class = BandForm
    extra_context = {'is_new':True}

    def handle_no_permission(self):
        return redirect(reverse('dashboard') + '?permissions=false')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = BandProfileImageForm(instance=self.object)
        return context

    def get_success_url(self):
        band = self.object
        band.owner = self.request.user
        band.save()
        return reverse('band_detail', kwargs={'pk':band.pk})


@login_required
def link_band(request, token):

    params = {
        'token': token
    }
    token = BandToken.objects.filter(token=token)
    if not token or not token[0].band or (token[0].expiration_date and token[0].expiration_date <= timezone.now()):
        params['badtoken'] = True
    else:
        band = token[0].band
        params['band'] = band

        if band.owner:
            params['has_owner'] = True
            if band.owner == request.user:
                params['user_owns'] = True

        if request.method == "POST":
            band.owner = request.user
            band.save()
            return  redirect('dashboard')

    return render(request, 'band/link.html', params)



def edit_band_token(request, token):
    token = BandToken.objects.filter(token=token)
    if not token or not token[0].band or (token[0].expiration_date and token[0].expiration_date >= timezone.now()):
        return render(request, 'band/badtoken.html', {'token': token})

    band = token[0].band
    save_success = False
    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, instance=band)
        if form.is_valid():
            band = form.save()
            save_success = True
    else:
        form = BandForm(instance=band)
    return render(request, 'band/edit_token.html', {'band':band, 'form': form, 'save_success': save_success })
