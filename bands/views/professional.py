import random

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from bands.forms.professional import ProfessionalForm
from bands.models import Professional, ProfessionalTag


def pro_list(request):

    pro_list = Professional.objects.all()

    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        pro_list = pro_list.filter(tag__pk=tag_filter)

    paginator = Paginator(pro_list, 6)
    page = request.GET.get('page')
    try:
        pros = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pros = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        pros = paginator.page(paginator.num_pages)

    if request.is_ajax():
        response = render(request, 'professional/search_results.html', {
            'pros': pros, 'page': page
        })
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        tags = ProfessionalTag.objects.filter(pro_tag__isnull=False).distinct()
        return render(request, 'professional/list.html', {
            'pros': pros, 'tags':tags, 'filtered_tags':None, 'page':page
        })

def pros_map_info(request):

    venues = Professional.objects.all().order_by('-latitude').select_related('tag').values('pk', 'name', 'latitude', 'longitude', 'profile_image', 'tag__name', 'tag__color')
    data = list(venues)
    return JsonResponse(data, safe=False, content_type="application/json")

def pro_detail(request, pk):
    pro = get_object_or_404(Professional, pk=pk)
    can_edit = False
    if request.user.is_authenticated():
        if request.user.is_superuser or (
                    request.user.has_perm('bands.manage_pro') and request.user == pro.user):
            can_edit = True

    return render(request, 'professional/detail.html', {
        'pro': pro,
        'can_edit':can_edit,
        'view': request.GET.get('view', None)
    })


@login_required
def pro_edit(request, pk):

    pro = get_object_or_404(Professional, pk=pk)

    can_edit = False
    if request.user.is_superuser or (
                request.user.has_perm('bands.manage_pro') and request.user == pro.user):
        can_edit = True

    if not can_edit:
        return redirect(reverse('pro_detail', kwargs={'pk':pro.pk} ) + '?permissions=false')

    if request.method == "POST":
        form = ProfessionalForm(request.POST, request.FILES, instance=pro)
        if form.is_valid():
            pro = form.save()
            return redirect('pro_detail', pk=pro.pk)
        else:
            print form.errors.as_data()
    else:
        form = ProfessionalForm(instance=pro)
    return render(request, 'professional/edit.html', { 'form': form, 'pro':pro })



@login_required
def pro_add(request):

    can_edit = False
    if request.user.is_superuser or request.user.has_perm('bands.manage_pro'):
        can_edit = True

    if not can_edit:
        return redirect( reverse('dashboard') + '?permissions=false' )

    if request.method == "POST":
        form = ProfessionalForm(request.POST, request.FILES)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.user = request.user
            pro.save()
            return redirect('pro_detail', pk=pro.pk)
        else:
            print form.errors.as_data()
    else:
        form = ProfessionalForm()
    return render(request, 'professional/edit.html', { 'is_new': True, 'form': form, 'pro':None })
